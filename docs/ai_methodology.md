**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

# Progress Report 2
## Grounded insight engine and public presentation
The second phase turns calculated facts into traceable explanations and enforces a clear public/private boundary. The supplied materials described a live-provider AI implementation that was absent from the ZIP and from the AI branch. This edition implements a working, offline insight engine and reports its actual capability: deterministic grounded explanations, with a tested optional selector interface. A live generative model is not configured or claimed as tested.

## Insight contract and evidence design
The engine receives an approved public snapshot containing analytics, risk/diversification and the aggregate Health Score. It constructs health, performance, concentration and diversification observations using only their exact source values. Each observation includes an ID, category, canonical text and a path/value evidence pair. For example, a concentration sentence cites risk.concentration.largest_holding_pct and the corresponding numeric value.

The engine does not calculate financial metrics, set risk thresholds, revise health-v2 or generate trading recommendations. A purchase-cost return is labelled as a snapshot measure rather than annual performance. Missing history produces an unavailable-history limitation rather than a fabricated volatility number. Company names and other free-text upload fields are never used as instructions or interpolated into generated insight prose.

## Provider boundary and deterministic fallback
An optional selector can reorder approved observation IDs. It receives a deep copy of the public facts and cannot mutate the canonical output. It must return every allowed ID exactly once. Unknown IDs, duplicate/missing IDs, non-list outputs and raised exceptions select the deterministic fallback. Arbitrary provider-authored text is never accepted. This avoids loose numeric checks that might accept an invented number merely because that number appears elsewhere in a portfolio.

There is no external API call, key configuration, cached provider response or provider charge in this release. Source is disclosed as deterministic, validated_selector or deterministic_fallback. The selector interface is tested with controlled functions; that is not a live AI-provider test. Any future generative provider requires its own implementation, consent/data-handling review and new tests.

## Public/private separation
The public upload envelope contains analytics, risk, approved input metadata and a compact Health Score. Public health exposes only score, band, full/partial basis, methodology version and generic limitations. It excludes component values, component drivers, missing-component names and private behavioural detail. GET /api/portfolio/behavior is removed from public routing and OpenAPI. Internal diagnostics remain callable from Python and from the controlled research harness; there is no unprotected diagnostic web endpoint.

The internal triage rule can place a supported concentration observation first. Its private trigger, concern value and flag do not enter the public fact set. Both normal and fallback outputs use the same canonical allowlist. health-v2 weights remain unchanged at 35% risk, 25% diversification, 25% behaviour and 15% performance, with unavailable component weights rescaled internally. Presentation filtering does not alter the numerical aggregate.

## Working client workflow
The local dashboard is served by FastAPI at /app/. It accepts required holdings plus optional transactions and price history, shows portfolio value, snapshot return, aggregate score, grounded explanations, holdings and data limitations, and exports the approved JSON analysis. It uses textContent for uploaded strings and rendered facts, so HTML in a symbol/company field does not become executable markup. It has loading, success, invalid-upload and network-error states and a mobile layout. No React build or external service is required.

The browser smoke test uploaded the sample holdings and transactions, rendered 12 holdings and displayed an aggregate Health Score of 72.43. Public behaviour diagnostics were absent. This confirms the tested local workflow; it is not a claim of production deployment or broad accessibility certification.

## Verification, delivery and limits
The supplied ZIP reproduces 312 passing tests and 20 passing subtests in this review environment. The earlier reports' 338-test claim could not be reproduced: the ZIP and GitHub AI branch did not contain the AI implementation described in Report 2. The revised project reproduces 359 passing tests and 20 passing subtests on CPython 3.12 and 3.14 with pandas 2.3.3. Counts are collected test outcomes, not a proxy for effort or product quality. Logs and JUnit records accompany the submission. No pandas 3 verification is claimed for this edition.

New tests validate each evidence value against its exact public path, reject malicious/invalid selector outputs, prevent selector mutation of canonical facts, avoid company-name prompt injection and recursively inspect public endpoint payloads and OpenAPI for private diagnostic names. Full internal outputs are separately tested for upload/readback equality. The UI consumes only these public responses; its JSON export does not call internal functions.

The insight layer communicates evidence; it does not prove investor comprehension or improved investment decisions. A live LLM, conversational portfolio Q&A, broker integration and personalised advice remain outside this implementation. There is no client-account authentication or multiuser isolation, so the dashboard is a localhost research demonstration with sample data.

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
