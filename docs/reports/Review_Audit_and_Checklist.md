**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

# Review audit and submission checklist
## Professor's requested evidence
| Requirement | Before audit | Current deliverable | Reproduction |
|---|---|---|---|
| Complete backend-file architecture | Brief folder-level document; some statements ahead of ZIP | Architecture report plus per-file inventory | docs/architecture.md and docs/file_inventory.json |
| Python code files | Engines/backend present; AI absent; main branch mostly overview | Integrated source tree, grounded insights, evaluation and tests | requirements-lock.txt; scripts/verify.ps1 |
| Backtesting results | No market backtesting package/results found in supplied ZIP/branches | 120 recorded historical runs and 152 pipeline checkpoints | python -m evaluation.run --verify |
| Win/loss ratio and viability | No complete trade ledger or reproducible metric definitions | Cost-aware closed-trade metrics, synthetic FIFO outcomes and viability assumptions | results/ and Backtesting evidence report |
| Independent rerun | Local venv/cache and database in ZIP; broad dependency bounds | Clean source, lock, offline Windows wheels, hashes and expected result | Tests then full frozen-output comparison |

## Material discrepancies corrected
The progress reports describe an AI module and 338 passing tests that were not present in the supplied code. The AI and frontend feature branches contained only skeleton files. Other feature branches contained module deliveries, and main remained an overview. The ZIP had a populated database and environment/cache files. These are not portable proof of functionality. Original material has been preserved; this edition integrates the actual code and reports newly reproduced results.

The existing behaviour privacy requirement was described as planned in all three progress reports. The old upload and health payloads and behaviour route still exposed private diagnostics. The review implements public allowlists, removes the public behaviour route, preserves internal calculations and supplies regression tests.

Historical risk no longer silently excludes missing securities or skips missing alignment, and initial capital is now included in maximum drawdown. Portfolio validation rejects non-finite values before JSON encoding. The AI placeholder is replaced with a deterministic evidence-based endpoint and a local dashboard. No unverified live-provider delivery is claimed.

## Verification record and scope
The supplied ZIP reproduces 312 passing tests and 20 passing subtests in this review environment. The earlier reports' 338-test claim could not be reproduced: the ZIP and GitHub AI branch did not contain the AI implementation described in Report 2. The revised project reproduces 359 passing tests and 20 passing subtests on CPython 3.12 and 3.14 with pandas 2.3.3. Counts are collected test outcomes, not a proxy for effort or product quality. Logs and JUnit records accompany the submission. No pandas 3 verification is claimed for this edition.

The baseline test suite is preserved in the original archive. Changes to API expectations are intentional contract migrations, documented in docs/api.md. Internal formulas and reference checks remain. New tests cover numerical accounting and the new privacy boundary. There are no newly introduced skipped or expected-failure tests. The dependency library emits a TestClient deprecation notice; it does not affect the passing assertions and remains visible in logs.

The backtest outcome is mixed and often adverse relative to buy-and-hold. Positive technical verification must not be described as profitable trading or commercial validation. Neither market-data accuracy nor source-document research claims have been externally audited.

## Source inventory and preservation
All four supplied PDFs were text-extracted and visually inspected on representative pages. Source PDFs are 10, 11, 15 and 9 pages respectively. The ZIP inventory was checked for modules, tests, data, documentation, cached files and environments. GitHub main and all seven feature branches were inspected. The source manifest records file hashes. Originals are copied unchanged into the pendrive package and remain separate from the current review edition.

## What the team must check before submitting
- Each member runs and understands their allocated package and confirms an accurate contribution statement. No equal historical effort is certified by this audit.
- Open the three revised progress reports, architecture report and backtesting evidence; confirm the course/team details and current review date.
- Run the clean-install verifier on the actual submission machine, save its local test output and retain the frozen expected artifact.
- Start the localhost demonstration, upload sample files, inspect invalid input handling and export public JSON.
- State the distinction between a snapshot return, synthetic realised P&L, market backtest and commercial viability.
- Do not replace unfavourable results, change costs or dates without recording the change and regenerating the reports.
- Confirm the actual Monday deadline with the course; the supplied message does not specify a date. This package does not infer a submission deadline.

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
