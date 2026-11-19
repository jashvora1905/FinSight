"""Offline evaluation: python -m evaluation.run [--output results] [--verify]."""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import gzip
from pathlib import Path
import numpy as np
import pandas as pd
from analytics import analyze_portfolio, compute_holdings, load_portfolio
from backend.services.analysis_service import run_analysis
from backend.services.joint_context import combined_context
from behavior.transaction_analysis import load_transactions
from risk_engine import analyze_portfolio_risk
from .backtest import run_backtest, validate_prices
from .realized import realized_performance

ROOT = Path(__file__).resolve().parents[1]


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False, sort_keys=True) + "\n", encoding="utf-8")


def save_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def evaluate():
    market = ROOT / "data/market"
    provenance = json.loads((market / "provenance.json").read_text())
    digest = hashlib.sha256((market / "prices.csv").read_bytes()).hexdigest()
    if digest != provenance["prices_sha256"]:
        raise ValueError("Frozen prices checksum mismatch")
    for s in provenance["series"]:
        if "error" in s:
            raise ValueError(f"Market download incomplete: {s['symbol']}")
        raw = market / (s["symbol"].replace("^", "") + ".json")
        if hashlib.sha256(raw.read_bytes()).hexdigest() != s["raw_sha256"]:
            raise ValueError("Raw market file checksum mismatch")
    frame = validate_prices(pd.read_csv(market / "prices.csv"))
    metrics, trades, curves = [], [], []
    for symbol, rows in frame.groupby("symbol"):
        series = rows.set_index("date")["close"]
        for label, start, end in [("development", "2020-01-01", "2022-12-31"),
                                   ("evaluation", "2023-01-01", "2025-12-31"),
                                   ("full", "2020-01-01", "2025-12-31")]:
            for strategy in ["buy_hold", "sma50"]:
                for cost in [0, 10, 25, 50]:
                    result = run_backtest(series, strategy=strategy, cost_bps=cost, start=start, end=end)
                    ident = {"symbol": symbol, "period": label}
                    metrics.append({**ident, **result["metrics"]})
                    if cost == 10:
                        tag = {**ident, "strategy": strategy}
                        trades.extend({**tag, **r} for r in result["trades"])
                        curves.extend({**tag, **r} for r in result["equity"])
    # Rolling no-future-data checkpoints exercise the actual FinSight engines.
    equity = frame[frame.symbol != "^NSEI"]
    pivot = equity.pivot(index="date", columns="symbol", values="close").dropna()
    sectors = {"RELIANCE.NS": "Energy", "TCS.NS": "IT", "HDFCBANK.NS": "Banking", "ITC.NS": "FMCG"}
    snapshots = []
    for index in range(126, len(pivot)-21, 21):
        history = pivot.iloc[index-126:index+1]
        now = history.iloc[-1]
        for kind in ["equal_weight", "concentrated"]:
            target = {s: 0.25 for s in pivot.columns}
            if kind == "concentrated":
                target = {s: (0.7 if s == "RELIANCE.NS" else 0.1) for s in pivot.columns}
            portfolio = pd.DataFrame([{"portfolio_id": kind, "symbol": s, "company_name": s,
                "asset_type": "Equity", "sector": sectors[s], "quantity": 100000*target[s]/now[s],
                "average_buy_price": history.iloc[0][s], "current_price": now[s]} for s in pivot.columns])
            prices = history.rename_axis("date").reset_index().melt(id_vars="date", var_name="symbol", value_name="close")
            analysis = run_analysis(portfolio, price_history=prices)
            # Forward observation is recorded only AFTER all score calculations.
            future = pivot.iloc[index+21]
            forward = sum(target[s] * (future[s]/now[s]-1) for s in target)*100
            snapshots.append({"date": str(history.index[-1].date()), "portfolio": kind,
                "health_score": analysis["health_score"]["score"],
                "risk_score": analysis["risk"]["risk_score"]["score"],
                "diversification_score": analysis["risk"]["diversification"]["diversification_score"],
                "annualized_volatility_pct": analysis["risk"]["risk_metrics"]["annualized_volatility_pct"],
                "maximum_drawdown_pct": analysis["risk"]["risk_metrics"]["maximum_drawdown_pct"],
                "forward_21_session_return_pct": round(float(forward),6),
                "score_basis": analysis["health_score"]["score_basis"]})
    sample = run_analysis(pd.read_csv(ROOT/"data/sample_portfolio.csv"),
                          load_transactions(ROOT/"data/sample_transactions.csv"))
    realized = realized_performance(load_transactions(ROOT/"data/sample_transactions.csv"), cost_bps=10)
    meta = {"methodology_version": "review-evaluation-v1", "data_sha256": digest,
            "periods": {"warmup": "2019", "development": "2020-2022", "evaluation": "2023-2025"},
            "market_runs": len(metrics), "pipeline_checkpoints": len(snapshots),
            "limitations": ["Retrospective holdout; not a previously untouched or prospective test.",
                "Convenience selection of surviving stocks; no delisted universe or corporate-event audit.",
                "Adjusted closes are total-return proxies; exact executable prices are not modeled.",
                "NIFTY 50 is a price index, excludes dividends and is not directly investable.",
                "Costs are per-side assumptions, not a tax or brokerage calculator.",
                "Health thresholds are heuristic; no predictive or commercial validity established."]}
    return {"metadata": meta, "metrics": metrics, "trades": trades, "curves": curves,
            "snapshots": snapshots, "sample_analysis": sample, "sample_realized": realized}


def compare(expected, actual, path="root"):
    if isinstance(expected, dict):
        if set(expected) != set(actual): raise ValueError(f"Keys differ at {path}")
        for key in expected: compare(expected[key], actual[key], path+"."+key)
    elif isinstance(expected, list):
        if len(expected) != len(actual): raise ValueError(f"Lengths differ at {path}")
        for i,(a,b) in enumerate(zip(expected,actual)): compare(a,b,f"{path}[{i}]")
    elif isinstance(expected, (int,float)) and not isinstance(expected,bool):
        if not np.isclose(expected, actual, rtol=1e-9, atol=1e-6): raise ValueError(f"Numeric mismatch at {path}: {expected} != {actual}")
    elif expected != actual:
        raise ValueError(f"Mismatch at {path}")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/"results")
    parser.add_argument("--verify", action="store_true")
    args=parser.parse_args()
    result=evaluate()
    if args.verify:
        compare(json.loads(gzip.decompress((ROOT/"results/expected.json.gz").read_bytes())), result)
        print("VERIFIED: all frozen inputs, metrics, trades, equity points and pipeline checkpoints match.")
        return
    args.output.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(result, allow_nan=False, sort_keys=True, separators=(",", ":")).encode()
    (args.output/"expected.json.gz").write_bytes(gzip.compress(payload,mtime=0))
    save_json(args.output/"metadata.json",result["metadata"])
    save_json(args.output/"sample_analysis_internal.json",result["sample_analysis"])
    save_json(args.output/"sample_realized.json",result["sample_realized"])
    for key in ["metrics","trades","curves","snapshots"]:
        save_csv(args.output/(key+".csv"),result[key])
    versions={p:importlib.metadata.version(p) for p in ["pandas","numpy","fastapi","pydantic","pytest","httpx","starlette","uvicorn","python-multipart"]}
    save_json(args.output/"environment.json",{"python":platform.python_version(),"platform":platform.platform(),"packages":versions})
    print(f"Wrote {len(result['metrics'])} market runs and {len(result['snapshots'])} pipeline checkpoints to {args.output}")


if __name__ == "__main__": main()
