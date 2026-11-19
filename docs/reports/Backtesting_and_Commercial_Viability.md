**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

# Backtesting and commercial viability evidence
## Evaluation question and interpretation
Can the supplied architecture be run repeatedly with traceable inputs, and can its performance accounting be independently checked? The answer is supported by frozen data, calculation tests, execution ledgers and exact-path reproduction checks. A separate question - whether the product or a trading rule is commercially successful - is not established by these engineering checks.

## Data and protocol
Daily Yahoo Finance chart responses were retrieved for RELIANCE.NS, TCS.NS, HDFCBANK.NS, ITC.NS and ^NSEI. Equity histories contain 1,730 observations each; NIFTY contains 1,727. The frozen interval is 1 January 2019 through 31 December 2025. The provider's adjusted close is used where supplied. Raw bytes, retrieval timestamp, endpoint URLs and SHA-256 values are recorded in data/market/provenance.json. These are provider-derived data, not an exchange-certified or point-in-time market database.

The protocol is fixed at a 50-session moving average. It is not tuned to maximise these results. Warm-up: 2019. Development: 2020-2022. Evaluation: 2023-2025. Full-period context: 2020-2025. This is a retrospective partition, not a genuinely untouched holdout. Both methods are evaluated on each series with zero, 10, 25 and 50 basis points of per-side cost, starting with INR 100,000, fractional units, no leverage, no shorting and zero cash interest.

## Accounting and metric definitions
Signals observed on close t-1 execute at close t, adding a full bar of latency. A buy invests cash divided by price times (1 + cost rate). A sale receives quantity times price times (1 - cost rate). Open units are marked daily and liquidated at the final close. A completed round trip is one trade. Win/loss is the count of positive net-P&L trades divided by negative net-P&L trades; zero-loss and no-trade cases return null with a reason. Win rate includes breakeven trades in its denominator. Profit factor is total positive net-P&L divided by the absolute negative net-P&L. Costs are already included in each trade P&L.

Total return is final equity divided by initial capital minus one. CAGR uses elapsed calendar days and 365.25 days per year. Volatility is sample standard deviation of recorded equity returns times sqrt(252). Sharpe uses zero cash rate; it is not a risk-free-rate-adjusted investment recommendation. Drawdown is the minimum wealth-to-running-peak ratio minus one, including initial capital and cost losses. Daily curves and trade P&Ls reconcile to final equity within rounding tolerance.

## Retrospective evaluation results: 2023-2025, 10 bps per side
| Series | Method | Return % | Max drawdown % | Wins / losses | Win rate % | Profit factor |
|---|---|---|---|---|---|---|
| HDFCBANK.NS | buy_hold | 26.23 | -19.91 | 1 / 0 | 100.00 | Undefined |
| HDFCBANK.NS | sma50 | -10.23 | -24.64 | 12 / 21 | 36.36 | 0.73 |
| ITC.NS | buy_hold | 39.49 | -20.32 | 1 / 0 | 100.00 | Undefined |
| ITC.NS | sma50 | 28.49 | -18.54 | 6 / 15 | 28.57 | 1.68 |
| RELIANCE.NS | buy_hold | 33.28 | -27.18 | 1 / 0 | 100.00 | Undefined |
| RELIANCE.NS | sma50 | 21.16 | -31.14 | 13 / 14 | 48.15 | 1.42 |
| TCS.NS | buy_hold | 7.16 | -34.45 | 1 / 0 | 100.00 | Undefined |
| TCS.NS | sma50 | 1.71 | -22.06 | 8 / 19 | 29.63 | 1.05 |
| ^NSEI | buy_hold | 43.30 | -15.77 | 1 / 0 | 100.00 | Undefined |
| ^NSEI | sma50 | 19.87 | -14.56 | 8 / 12 | 40.00 | 1.84 |

The SMA method does not outperform buy-and-hold in this selected sample. Results must be assessed together: high profit factor can coexist with a low win rate; a positive total return can coexist with a deep drawdown; a one-trade benchmark cannot establish a stable win probability. No pooled portfolio return is implied by summing separate single-security experiments.

## Cost sensitivity: SMA, evaluation period
| Series | 0 bps return % | 10 bps return % | 25 bps return % | 50 bps return % |
|---|---|---|---|---|
| HDFCBANK.NS | -4.11 | -10.23 | -18.69 | -31.06 |
| ITC.NS | 34.01 | 28.49 | 20.65 | 8.62 |
| RELIANCE.NS | 27.89 | 21.16 | 11.74 | -2.38 |
| TCS.NS | 7.36 | 1.71 | -6.20 | -18.05 |
| ^NSEI | 24.76 | 19.87 | 12.88 | 2.14 |

Costs materially reduce active-strategy returns. The bps model combines assumed trading friction; it does not model actual brokerage schedules, STT, GST, stamp duty, capital-gains tax, bid/ask variation, liquidity constraints, circuit limits, partial fills or exact corporate-action execution. Adjusted historical prices themselves may be revised by the vendor. Frozen files ensure reproducibility of this edition, not correctness of every provider observation.

## Synthetic sample transaction outcomes
At 10 basis points per side, the included sample has four fully matched sale transactions, one winner, three losers, zero breakeven sales, 25% win rate, 0.333333 win/loss ratio, 0.291193 profit factor and INR -2,849.90 net realised P&L. A sell matching several buy lots is counted once. A partly unmatched sell is excluded in full and listed for reconciliation. Open positions are excluded. These synthetic outcomes are not a historical market strategy backtest and cannot validate demand or profitability.

## Commercial viability: evidence versus assumptions
The prototype has deterministic local analysis, no recurring model cost in its current offline mode, a functioning demonstration and reproducible evaluation. No audited paying customers, conversion data, retention, acquisition cost, support cost, market-data contract or compliance budget is supplied. The earlier report's 8-10 versus 12 interviews, 100% adoption intent, 75% willingness-to-pay and competing INR 8 lakh/2 crore/2-3 crore asks cannot be independently verified from these materials.

An illustrative subscription case at INR 499 per month, INR 80 variable cost, 3% payment fee and INR 15,000 fixed monthly cost gives INR 404.03 contribution per paid user and 38 paid users to cover those assumed fixed costs. These are scenario inputs, not quotes or validated forecasts. Acquisition, tax, founder salaries, licensed data and compliance can change the outcome substantially. If contribution is non-positive, there is no finite break-even user count in this model. evaluation/business_case.py makes the assumptions editable.

Next evidence should include permissioned interview records, a clearly defined customer segment, observed prototype task completion, measured willingness-to-pay, a small paid pilot, actual operating quotes, retention and support burden, and a current assessment of the intended commercial service. No marks increase, investment return or business outcome is promised.

## Reproduction and examiner check
Run scripts/verify.ps1 from the extracted FinSight folder. Use -Offline with -PythonVersion 3.12 or 3.14 when the corresponding 64-bit Windows Python is installed. Offline wheel folders accompany the pendrive copy. For other systems, install requirements-lock.txt using the appropriate Python environment. After dependencies are installed, tests and evaluation require no market-data or AI network calls.

Read results/metrics.csv, trades.csv, curves.csv, snapshots.csv and sample_realized.json. The files named internal are evaluator diagnostics and are not user dashboard exports. A different dataset, vendor adjustment, date range, price convention, execution lag or cost setting produces a different experiment; compare the frozen baseline first and then document each variation.
