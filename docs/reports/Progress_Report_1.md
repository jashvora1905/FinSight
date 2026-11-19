**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

# Progress Report 1
## Analytics, risk and transaction engines
The first phase establishes deterministic calculation modules, explicit input contracts and independently checkable outputs. A portfolio snapshot answers valuation and exposure questions; transaction history answers matched realised-outcome questions; market history supports historical volatility and drawdown. These are different evidence types and are not interchangeable.

## Implemented scope and engineering decisions
The analytics engine validates the eight-column holdings contract, calculates invested and current value, absolute profit/loss, purchase-cost return, holding weights, sector allocation and asset-type allocation. Duplicate positions are merged using quantity-weighted purchase cost; zero-quantity rows are skipped with warnings. Missing or zero current prices use purchase cost with an explicit missing-price flag. This is a convenience for incomplete academic data, not a market valuation estimate. Missing purchase cost is rejected.

The review adds engine-level rejection of blank portfolio identifiers, infinite quantities/prices and overflowed holding values. Rejecting these before JSON serialization prevents misleading results or opaque server errors. Shared loading rules are used for upload and subsequent SQLite readback.

The risk engine calculates largest holding and sector percentages, top-three concentration, Herfindahl indices, effective holdings, diversification scores, historical volatility, drawdown and covariance risk contributions where usable history is present. The prototype risk score is higher when measured risk is higher; the Health Score is higher when its heuristic dimensions are healthier. They are not the same score.

## Historical-risk corrections
Previously, missing securities could be silently dropped and the remaining weights renormalised. The revised engine requires every holding symbol on every supplied observation date. Duplicate date/symbol pairs, malformed dates, non-positive and non-finite prices disable historical results with an explicit reason. No price interpolation or silent forward filling is used. Unavailable history does not become zero volatility.

The drawdown running peak now includes initial wealth of 1.0. A path 100 -> 90 -> 80 must report -20% maximum drawdown; ignoring the starting value understates this first-period loss. A hand-worked regression test checks this exact case. Volatility is sample daily standard deviation times sqrt(252). Historical portfolio returns use current snapshot weights held constant across the window, equivalent to a daily rebalanced exposure proxy, not a reconstruction of the investor's actual past holdings.

## Transaction and behaviour analysis
Transaction validation requires unique transaction IDs per portfolio, ISO dates, BUY/SELL, finite positive quantities and prices. FIFO matches each sale to preceding purchase lots, respecting input order on the same date. Opening inventory, short positions, taxes and corporate-action adjustments are not inferred. Unmatched sales are disclosed internally and prevent an unsupported complete-history assessment.

The experimental behaviour score remains internal. It requires sufficient observation length, trade count and matched history. It is a heuristic flag aggregation, not a psychological diagnosis or validated measure of investor skill. Cross-symbol share-quantity weighting can be affected by denomination; this limitation remains explicit. The internal joint context prioritises exposure review when high concentration coincides with supported concerns. It never adds a second numerical penalty to health-v2.

## Reproduced sample outputs
| Measure | Reproduced value | Interpretation |
|---|---|---|
| Invested value | INR 1,066,849.80 | Supplied purchase cost of current holdings |
| Current value | INR 1,190,594.75 | Supplied prices, not live quotes |
| Snapshot P&L | INR 123,744.95 | Current minus invested value |
| Purchase-cost return | 11.60% | Not CAGR, XIRR or time-weighted return |
| Risk score | 33.75 | Prototype concentration-based score without history |
| Diversification score | 80.98 | Prototype breadth/concentration heuristic |
| Aggregate Health Score | 72.43 | health-v2; experimental composite |

The independent FIFO realised-outcome analysis of the synthetic sample yields four fully matched sale transactions: one profitable and three loss-making after 10 basis points per side, a 25% win rate and a 1:3 win/loss count. Net realised P&L is INR -2,849.90. Open holdings are excluded. This does not contradict the positive snapshot P&L: the snapshot and the closed sales describe different positions and denominators. The sample holdings and transactions are independent fixtures, not a reconciled broker account.

## Verification and remaining limits
The supplied ZIP reproduces 312 passing tests and 20 passing subtests in this review environment. The earlier reports' 338-test claim could not be reproduced: the ZIP and GitHub AI branch did not contain the AI implementation described in Report 2. The revised project reproduces 359 passing tests and 20 passing subtests on CPython 3.12 and 3.14 with pandas 2.3.3. Counts are collected test outcomes, not a proxy for effort or product quality. Logs and JUnit records accompany the submission. No pandas 3 verification is claimed for this edition.

Tests cover hand-calculated valuation, missing and invalid inputs, duplicate merging, concentration, sample behaviour, provisional scoring, full internal storage parity, strict historical coverage and initial-peak drawdown. The new backtest tests independently verify cash accounting, entry/exit cost arithmetic, one-bar execution delay and absence of future-price influence on earlier positions.

Diversification full-credit thresholds and score weights are prototype assumptions. The engine does not inspect fund constituents, estimate client suitability, audit exchange data or establish that a high score predicts returns. These are retained as limitations rather than overstated as completed commercial capabilities.

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
