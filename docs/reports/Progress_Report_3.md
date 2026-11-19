**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

# Progress Report 3
## Backend integration, reproducibility and evaluation
The third phase packages the complete working architecture, Python modules, repeatable evaluation outputs and review instructions. The key acceptance condition is that another machine can rerun the same frozen inputs and compare all outputs. It is not sufficient for screenshots or isolated headline numbers to look plausible.

## Integrated architecture
CSV input -> FastAPI upload router -> decoding and schema validation -> deterministic analytics/risk/transaction engines -> health-v2 -> atomic SQLite replacement. Read endpoints reload the stored rows and recompute analysis. Public allowlist functions then return approved analytics, exposure, aggregate health and grounded insight payloads. Internal transaction diagnostics and joint-context flags stay in the research layer.

FastAPI contains routers, typed public schemas, services, configuration and SQLite repository functions. SQL writes use bound parameters and an atomic transaction. Re-uploading replaces holdings, transactions and history for the affected portfolio IDs. Validation happens before persistence. The database is created on first use and is not shipped pre-populated. This prevents an old local database from becoming an unexplained source of review results.

Expected failures use a consistent detail response with 4xx status. Unexpected exceptions are logged on the server and return a generic 500. Files are UTF-8 CSV, limited to 5 MB each. The application should bind to 127.0.0.1 for the academic demonstration. It is a single-user local prototype with no account-level access control, rate limiting or production backup service.

## Current public API
| Method | Path | Purpose |
|---|---|---|
| GET | /health | Liveness only |
| POST | /api/portfolio/upload | Validate/store data and return public analysis |
| GET | /api/portfolio/summary | Holdings snapshot totals |
| GET | /api/portfolio/holdings | Per-holding valuation |
| GET | /api/portfolio/performance | Snapshot performance |
| GET | /api/portfolio/allocation | Asset/sector/security allocation |
| GET | /api/portfolio/risk | Exposure and available historical risk |
| GET | /api/portfolio/diversification | Diversification outputs |
| GET | /api/portfolio/health | Aggregate score only |
| GET | /api/portfolio/insights | Grounded public explanations |
| GET | /app/ | Local dashboard |

## Backtesting and win/loss results
The evaluation includes 120 market runs: five series, two methods, three periods and four cost assumptions. The warm-up data is 2019; the retrospective development period is 2020-2022; the retrospective evaluation period is 2023-2025. Every strategy uses the same inputs and accounting rules. The comparison is buy-and-hold versus a fixed 50-session moving-average long/cash research rule. A signal observed at the previous close executes at the next close; exposure earns subsequent returns. All end positions are liquidated and both-side costs are charged.

This is a research benchmark, not a FinSight trading recommendation or proof of predictive capability. The evaluation split was declared during this audit, not locked before seeing the historical period. The convenience universe excludes delisted stocks and creates survivorship bias. Adjusted closes are total-return proxies; NIFTY is a price index, so the same-stock buy-and-hold comparisons are the primary baselines.

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

At 10 basis points per side, the SMA method underperforms its own buy-and-hold baseline on all five series in the evaluation period. HDFC Bank's SMA result loses capital; drawdown is also worse than buy-and-hold for HDFC Bank and Reliance. These adverse results are retained. Buy-and-hold has only one terminally closed trade per period, so a 100% win rate is not meaningful evidence of a robust strategy and its no-loss win/loss denominator is reported as undefined.

## Pipeline replay and reproducibility
The runner also replays 152 checkpoints through the actual FinSight engines: equal-weight and concentrated four-stock snapshots over trailing 126-return windows, sampled every 21 sessions. The score is calculated using only history available at that checkpoint; the forward 21-session return is recorded afterward for exploratory inspection. The aggregate score remains partial without transaction evidence. These checkpoints demonstrate repeatable operation, not calibration or causal validation of the score.

Frozen prices, raw provider responses, provenance, data hashes, every market metric, execution ledger, daily equity curve and pipeline checkpoint are included. The compact expected artifact stores the complete reference result. python -m evaluation.run --verify checks the input hashes and recursively compares values with absolute tolerance 1e-6 and relative tolerance 1e-9. It exits nonzero on a mismatch and identifies its path. Test and environment records accompany the report.

## Verification record
The supplied ZIP reproduces 312 passing tests and 20 passing subtests in this review environment. The earlier reports' 338-test claim could not be reproduced: the ZIP and GitHub AI branch did not contain the AI implementation described in Report 2. The revised project reproduces 359 passing tests and 20 passing subtests on CPython 3.12 and 3.14 with pandas 2.3.3. Counts are collected test outcomes, not a proxy for effort or product quality. Logs and JUnit records accompany the submission. No pandas 3 verification is claimed for this edition.

The updated public API deliberately changes the original contract: private diagnostics are removed, the previous 501 insights placeholder becomes a working endpoint, and health responses are reduced to the approved public schema. Tests for those old expectations were updated to the new documented contract, while internal formula, FIFO, storage and reference checks remain active. No failing tests were marked as passing or skipped to increase the count.

## Commercial interpretation
The technical evidence supports a reproducible academic analytics prototype. It does not demonstrate product-market fit, profitable trading, regulatory registration or operational readiness. Original survey percentages, interview counts, market-size estimates and funding asks are inconsistent or lack source records, so they are not used as validated traction. A separate commercial viability note distinguishes assumptions from evidence and defines the next validation work.

This technical review makes no regulatory-compliance claim. Commercial use needs a separate current assessment of the actual service, data licences and applicable obligations.

## Fair seven-member allocation
This is a proposed review-work allocation, with an equal target share of 1/7 (approximately 14.29%) for each member across implementation, verification and documentation. Equal percentages describe the workload plan, not measured historic hours or a claim that everyone wrote equal code. Each member must execute and explain their package before signing a contribution statement. The available Git history uses Jash as the committer for several module imports; it cannot establish individual effort. No invented hours, commits, authorship or completed member-specific checks are asserted here.

| Member | Work package | Phase 1 evidence | Phase 2 evidence | Phase 3 evidence |
|---|---|---|---|---|
| Rayyan Chunawala (E014) | Insights and evidence grounding | Metric vocabulary; approved evidence paths; explanation templates | Selector validation; fallback; prompt-injection checks | Evidence trace review; wording audit; explanation demonstrations |
| Ricky Maishari (E037) | User workflow and presentation | Upload journey; API contract mapping; error-state design | Dashboard; safe rendering; public JSON export | Desktop/mobile checks; UI walkthrough; presentation evidence |
| Prisha Mistry (E042) | Transaction integrity and realised outcomes | Transaction schema; FIFO scenarios; missing-history policy | Behaviour diagnostics; sell-level outcomes; unmatched-sell handling | FIFO reconciliation; non-disclosure checks; transaction limitations |
| Soumil Patro (E050) | Risk and historical methodology | Concentration definitions; historical coverage; baseline drawdown | Historical-risk fixes; cross-engine triage; cost sensitivity review | Risk reference checks; drawdown interpretation; methodology defence |
| Aditya Shah (E062) | Analytics and backtest accounting | Holding valuation; return denominators; finite-value rules | Valuation validation; backtest ledger; snapshot calculations | Hand calculations; capital reconciliation; return interpretation |
| Atharva Suryavanshi (E065) | Data provenance and reproducibility | Source inventory; frozen data; edge-case planning | Evaluation runner; checksums; CI and portable setup | Clean-install rerun; artifact comparison; regression evidence |
| Jash Vora (E067) | Backend architecture and integration | File contracts; database semantics; error boundaries | Routers/services; public schemas; storage integration | Endpoint tests; architecture inventory; complete demo integration |

Every package has the same acceptance obligations: understand the design, review the relevant code, execute positive and failure cases, reproduce the evidence, document a limitation, and cross-review another package. Suggested review ring: Rayyan -> Ricky -> Prisha -> Soumil -> Aditya -> Atharva -> Jash -> Rayyan. The technical deliverables below were prepared during this assisted review; the table assigns ownership for team verification rather than retrospectively attributing those edits.
