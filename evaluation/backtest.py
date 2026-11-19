"""Close-to-close, long/cash research backtest with a full execution ledger.

Signals observed at close t-1 execute at close t; holdings earn returns starting
after execution. This deliberately adds a full bar of latency. Adjusted prices
are total-return proxies, not tradable quotes. See docs/backtesting.md.
"""
from __future__ import annotations

import math
import numpy as np
import pandas as pd


def validate_prices(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "symbol", "close"}
    if not required <= set(frame):
        raise ValueError("Prices require date,symbol,close")
    df = frame.copy()
    df["date"] = pd.to_datetime(df["date"], errors="raise")
    if df["date"].isna().any() or df["symbol"].isna().any():
        raise ValueError("Dates and symbols cannot be missing")
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df["close"] = pd.to_numeric(df["close"], errors="raise")
    if (df["symbol"] == "").any() or not np.isfinite(df["close"]).all() or (df["close"] <= 0).any():
        raise ValueError("Prices must be finite and positive; symbols nonempty")
    if df.duplicated(["date", "symbol"]).any():
        raise ValueError("Duplicate date/symbol prices")
    return df.sort_values(["date", "symbol"]).reset_index(drop=True)


def win_loss(pnls, tolerance=1e-8) -> dict:
    p = np.asarray(list(pnls), dtype=float)
    if not np.isfinite(p).all():
        raise ValueError("Non-finite P&L")
    wins, losses = p[p > tolerance], p[p < -tolerance]
    n = len(p)
    return {
        "closed_trades": n, "wins": len(wins), "losses": len(losses),
        "breakeven": int(n - len(wins) - len(losses)),
        "win_rate_pct": round(100 * len(wins) / n, 6) if n else None,
        "win_loss_ratio": round(len(wins) / len(losses), 6) if len(losses) else None,
        "win_loss_ratio_status": "defined" if len(losses) else "undefined_no_losses",
        "gross_profit": round(float(wins.sum()), 6),
        "gross_loss": round(float(-losses.sum()), 6),
        "profit_factor": round(float(wins.sum() / -losses.sum()), 6) if len(losses) else None,
        "expectancy_per_trade": round(float(p.mean()), 6) if n else None,
    }


def run_backtest(prices: pd.Series, *, strategy="sma50", window=50,
                 cost_bps=10.0, initial_capital=100000.0, start=None, end=None) -> dict:
    """One security, fractional units, no leverage/shorts, cash interest zero.

    Per-side cost combines assumed fees/slippage. A sell pays cost on proceeds.
    End-date liquidation closes every trade and is included in equity/drawdown.
    """
    if strategy not in {"sma50", "buy_hold"}:
        raise ValueError("strategy must be sma50 or buy_hold")
    if not isinstance(window, int) or window < 2:
        raise ValueError("window must be an integer >= 2")
    if not math.isfinite(cost_bps) or not 0 <= cost_bps < 10000:
        raise ValueError("cost_bps must be finite and in [0,10000)")
    if not math.isfinite(initial_capital) or initial_capital <= 0:
        raise ValueError("initial_capital must be finite and positive")
    p = prices.astype(float).sort_index()
    if p.index.has_duplicates or not isinstance(p.index, pd.DatetimeIndex) or p.index.hasnans:
        raise ValueError("Unique valid DatetimeIndex required")
    if not np.isfinite(p).all() or (p <= 0).any():
        raise ValueError("Prices must be finite and positive")
    # Shift BEFORE slicing so warm-up uses only earlier prices.
    target = ((p > p.rolling(window, min_periods=window).mean()).shift(1, fill_value=False)
              if strategy == "sma50" else pd.Series(True, index=p.index))
    selected = p.loc[start:end]
    if len(selected) < 2:
        raise ValueError("At least two evaluation observations are required")
    rate = cost_bps / 10000
    cash, units, entry, total_cost = initial_capital, 0.0, None, 0.0
    ledger, equity = [], []
    for k, (date, price) in enumerate(selected.items()):
        want = bool(target.loc[date]) and k < len(selected) - 1
        if units and not want:
            proceeds = units * price
            fee = proceeds * rate
            cash = proceeds - fee
            total_cost += fee
            ledger.append({**entry, "exit_date": date.date().isoformat(),
                           "exit_price": float(price), "quantity": units,
                           "exit_cost": fee, "net_pnl": cash - entry["cash_committed"],
                           "net_return_pct": (cash / entry["cash_committed"] - 1) * 100,
                           "exit_reason": "end_of_test" if k == len(selected)-1 else "signal"})
            units, entry = 0.0, None
        elif not units and want:
            committed = cash
            units = cash / (price * (1 + rate))
            fee = units * price * rate
            total_cost += fee
            entry = {"entry_date": date.date().isoformat(), "entry_price": float(price),
                     "entry_cost": fee, "cash_committed": committed}
            cash = 0.0
        equity.append({"date": date.date().isoformat(), "equity": cash + units * price,
                       "units": units, "cash": cash, "target": int(want)})
    curve = np.r_[initial_capital, [x["equity"] for x in equity]]
    rets = curve[1:] / curve[:-1] - 1
    dd = curve / np.maximum.accumulate(curve) - 1
    days = (selected.index[-1] - selected.index[0]).days
    std = np.std(rets, ddof=1)
    stats = {"strategy": strategy, "window": window, "cost_bps_per_side": cost_bps,
             "initial_capital": initial_capital, "final_equity": float(curve[-1]),
             "start": selected.index[0].date().isoformat(), "end": selected.index[-1].date().isoformat(),
             "observations": len(selected), "total_return_pct": (curve[-1] / initial_capital - 1) * 100,
             "cagr_pct": ((curve[-1] / initial_capital) ** (365.25 / days) - 1) * 100 if days else None,
             "annualized_volatility_pct": std * np.sqrt(252) * 100,
             "sharpe_zero_cash_rate": float(np.mean(rets) / std * np.sqrt(252)) if std > 1e-12 else None,
             "maximum_drawdown_pct": float(dd.min() * 100), "total_cost": total_cost,
             "exposure_pct": 100 * sum(x["units"] > 0 for x in equity) / len(equity),
             **win_loss(x["net_pnl"] for x in ledger)}
    stats = {k: round(float(v), 6) if isinstance(v, (float, np.floating)) else v for k,v in stats.items()}
    return {"metrics": stats, "trades": ledger, "equity": equity}
