**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

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
