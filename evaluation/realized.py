"""FIFO realized P&L on supplied transactions, independent of strategy backtests."""
from behavior.transaction_analysis import validate_transactions, holding_analysis
from .backtest import win_loss


def realized_performance(records, portfolio_id=None, cost_bps=0):
    if not 0 <= cost_bps < 10000:
        raise ValueError("cost_bps must be in [0,10000)")
    rows = validate_transactions(records, portfolio_id)
    holdings = holding_analysis(rows, rows[-1]["date"]) if rows else {"matches": [], "unmatched_sells": [], "open_lots": []}
    # One outcome per fully matched SELL transaction, even when it closes several lots.
    invalid = {r["transaction_id"] for r in holdings["unmatched_sells"]}
    sells = {}
    for m in holdings["matches"]:
        key = m["sell_transaction_id"]
        if key in invalid:
            continue
        pnl = m["quantity"] * (m["sell_price"] - m["buy_price"])
        fee = m["quantity"] * (m["sell_price"] + m["buy_price"]) * cost_bps / 10000
        sells[key] = sells.get(key, 0) + pnl - fee
    return {"basis": "fully_matched_sell_transactions_FIFO", "cost_bps_per_side": cost_bps,
            **win_loss(sells.values()), "net_realized_pnl": round(sum(sells.values()), 6),
            "excluded_unmatched_sell_ids": sorted(invalid), "open_lots": holdings["open_lots"],
            "outcomes": [{"sell_transaction_id": k, "net_pnl": v} for k,v in sells.items()],
            "limitation": "Sample transactions are synthetic; this is not market backtest evidence. Open positions excluded."}
