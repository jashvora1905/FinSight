**FinSight - Portfolio Health Intelligence Platform**

SVKM's NMIMS, Mukesh Patel School of Technology Management & Engineering (MPSTME). B.Tech Computer Science and Business Systems, Year 3, Semester V. Current review edition: 19 November 2026, Academic Year 2026-27. Original submitted documents retain their original dates and Semester IV context. This edition describes the current audited code and must not be backdated.

# Complete backend architecture
## Boundaries and execution flow
The application is a local single-user analytics prototype. The database holds supplied rows, not cached score truth. An upload validates all requested inputs and runs the analysis before committing a replacement transaction. A read reloads stored data and recomputes outputs. Public presentation then removes private diagnostics. No public endpoint offers order execution, broker connectivity or personalised recommendations.

1. backend/main.py creates FastAPI, lifespan initialization, exception handling, CORS and routes; it serves the local frontend at /app/.
2. backend/api/portfolio.py reads bounded UTF-8 CSV files and delegates to upload_service. Routes also expose valuation/allocation views.
3. upload_service parses CSVs, validates shared contracts through run_analysis and prepares repository dataclasses. Failed validation persists nothing.
4. analysis_service calls analytics, risk_engine and behavior, then compute_health_score. Public routes never serialize the full internal result directly.
5. repository.replace_portfolios atomically replaces selected portfolios and their dependent rows; load_scope reconstructs input frames and records.
6. presentation.public_upload and public_health enforce explicit output allowlists. Public insights consume that reduced data and optional private prioritisation only.
7. evaluation.run is an offline research harness. It exercises both the portfolio pipeline and a separately labelled strategy-accounting benchmark.

## Layer contracts
| Layer | Inputs | Outputs and failure policy |
|---|---|---|
| Analytics | Eight-column holdings table, optional portfolio selection | JSON-safe valuation/allocation/warnings; invalid data raises PortfolioDataError |
| Risk | Clean holdings and optional long-form price history | Concentration, diversification, risk score; unavailable historical fields carry a reason |
| Transactions | Validated BUY/SELL rows and observation dates | Internal FIFO/frequency/heuristic diagnostics; incomplete history remains explicit |
| Health | Validated engine outputs | health-v2 aggregate and internal components; unavailable dimensions rescale weights |
| Presentation | Full internal result | Public aggregate/valuation/exposure only; no private component serialization |
| Insights | Public metric snapshot | Canonical text with exact-path evidence; invalid selector falls back |
| Persistence | Dataclasses with raw accepted rows | Atomic SQLite writes and ordered readback |

## Persistence model
SQLite tables are users (currently unused), portfolios, holdings, transactions and price_history. Portfolios carry observation-window fields and upload timestamps; dependent records cascade when replaced. The schema uses local application IDs and no authentication context. Transactions and prices preserve source order needed by the analysis rules. Duplicate transaction IDs are rejected by validation rather than a historical audit log. The supplied database is excluded from the refined runtime package; it is generated on first use.

Replacing a portfolio overwrites the last input set; this is not an immutable run registry. The review artifacts provide a frozen, hashed experiment, but routine interactive uploads do not create permanent audit records. Backups, migration management, concurrent multiuser ownership and user deletion/retention workflows are future engineering work.

## Private diagnostics and security scope
Detailed behaviour results and component-level Health Score explanations remain available only through internal Python functions and evaluator artifacts. The old behaviour web route is not registered. There is no optional public switch to reveal these fields. OpenAPI and all public responses are regression-tested. Public health retains the aggregate score, full/partial basis and generic caveats; the internal formula is unchanged.

Inputs are untrusted data. SQL uses parameter binding; generated insight prose does not interpolate company-name instructions; the dashboard renders data with textContent. Upload sizes are bounded and unexpected errors are generic. These controls do not make the application production-ready: the localhost prototype has no login, account isolation, public-facing throttling, TLS service, penetration test or regulated-service operating controls.

## Historical-risk and backtest semantics
The risk module uses current weights over aligned trailing prices as a constant-weight historical exposure proxy. The strategy backtest maintains actual fractional units and cash for one security per experiment. Their returns and drawdowns have different definitions and must not be compared as if they describe the same managed portfolio. Snapshot buy prices are supplied inputs, not inferred from complete transaction histories.

## Complete production Python-file inventory
The table is generated from the actual source tree. docs/file_inventory.json additionally records exact hashes, public/private function names, classes and direct imports for every listed file. Empty __init__ files remain part of package wiring. Test files are supplied separately with JUnit evidence.

| File | Lines | Responsibility |
|---|---|---|
| ai/__init__.py | 3 | Package exports and module wiring. |
| ai/insight_engine.py | 49 | Grounded offline explanations; an optional selector reorders approved facts only. |
| analytics/__init__.py | 43 | FinSight Portfolio Analytics (owner: Aditya Shah, branch feature/portfolio-analytics). |
| analytics/allocation.py | 59 | Asset, sector and security allocation. |
| analytics/calculations.py | 68 | Basic, reusable financial formulas used across the analytics module. |
| analytics/performance.py | 72 | Stock-level and portfolio-level performance. |
| analytics/portfolio_metrics.py | 230 | Portfolio metrics: loading and validating portfolio data, building the |
| backend/__init__.py | 1 | FinSight backend (owner: Jash Vora, branch feature/backend). Layout follows the project README. |
| backend/api/__init__.py | 0 | Package exports and module wiring. |
| backend/api/behavior.py | 20 | GET /api/portfolio/behavior. |
| backend/api/health.py | 18 | GET /api/portfolio/health: the Portfolio Health Score (methodology health-v2). |
| backend/api/insights.py | 22 | Public grounded explanations. Private diagnostics remain Python-only. |
| backend/api/portfolio.py | 70 | POST /api/portfolio/upload and the portfolio analytics endpoints (README: API Structure). |
| backend/api/risk.py | 21 | GET /api/portfolio/risk and /api/portfolio/diversification. |
| backend/config.py | 17 | Backend settings. Everything can be overridden with environment variables. |
| backend/database/__init__.py | 3 | Package exports and module wiring. |
| backend/database/connection.py | 78 | SQLite connection + schema. |
| backend/database/repository.py | 118 | All SQL lives here. Uploads REPLACE the stored data of every portfolio_id they contain, so a stored portfolio |
| backend/main.py | 71 | FinSight FastAPI app. Run from the repository root: |
| backend/models/__init__.py | 3 | Package exports and module wiring. |
| backend/models/portfolio.py | 49 | Row models for the SQLite tables (README: Database Structure). Plain dataclasses, no ORM. |
| backend/schemas/__init__.py | 10 | Package exports and module wiring. |
| backend/schemas/behavior.py | 18 | Behaviour response (behavior, Prisha). |
| backend/schemas/common.py | 16 | Package exports and module wiring. |
| backend/schemas/health.py | 50 | Health Score response (health-v2, backend/services/health_score.py). |
| backend/schemas/portfolio.py | 104 | Portfolio analytics responses (analytics, Aditya) and the upload envelope. |
| backend/schemas/public.py | 23 | Public schema intentionally omits private diagnostic components. |
| backend/schemas/risk.py | 44 | Risk & diversification responses (risk_engine, Soumil). |
| backend/services/__init__.py | 0 | Package exports and module wiring. |
| backend/services/analysis_service.py | 57 | Glue between stored/uploaded data and the teammates' modules. No financial logic lives here: |
| backend/services/errors.py | 8 | One error type for every expected failure, so clients always get {"detail": "<message>"}. |
| backend/services/health_score.py | 212 | FinSight Health Score, methodology health-v2 (README: Portfolio Health Score). |
| backend/services/joint_context.py | 14 | Internal prioritisation only. Never changes health-v2 or produces public text. |
| backend/services/presentation.py | 15 | Explicit public allowlists. Internal diagnostics never cross this boundary. |
| backend/services/upload_service.py | 104 | CSV upload: read -> validate (via the analysis modules) -> store -> return the analysis. |
| behavior/__init__.py | 6 | Deterministic transaction-based behaviour analysis for FinSight. |
| behavior/__main__.py | 27 | Run with: python -m behavior path/to/transactions.csv --portfolio-id P001. |
| behavior/behavior_score.py | 96 | Public entry point and transparent experimental scoring methodology. |
| behavior/panic_selling.py | 33 | Short-hold loss-selling proxy; does not infer investor emotions. |
| behavior/trading_frequency.py | 24 | Trade frequency and a configurable high-activity proxy. |
| behavior/transaction_analysis.py | 149 | Validation, transaction summaries, and FIFO holding-duration analysis. |
| data/generate_sample_data.py | 150 | Regenerates every CSV in data/. Run from repo root: python data/generate_sample_data.py |
| evaluation/__init__.py | 1 | Reproducible research tools; no order execution or investment recommendations. |
| evaluation/backtest.py | 118 | Close-to-close, long/cash research backtest with a full execution ledger. |
| evaluation/business_case.py | 13 | Illustrative unit economics, never a claim of validated demand or actual costs. |
| evaluation/realized.py | 25 | FIFO realized P&L on supplied transactions, independent of strategy backtests. |
| evaluation/run.py | 144 | Offline evaluation: python -m evaluation.run [--output results] [--verify]. |
| risk_engine/__init__.py | 14 | FinSight Risk & Diversification Engine. |
| risk_engine/concentration.py | 78 | Concentration metrics for the FinSight risk engine. |
| risk_engine/diversification.py | 73 | Diversification analysis for FinSight. |
| risk_engine/risk_metrics.py | 140 | Historical risk metrics for FinSight. |
| risk_engine/risk_score.py | 144 | Prototype risk scoring for FinSight. |

## Operational entry points
Run python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 from the FinSight root. Open /app/ for the demo and /docs for the public API. Run python -m pytest -q for the complete suite. Run python -m evaluation.run --verify to compare the frozen experiment. Run python -m evaluation.run --output results_new for a separate regeneration; preserve the original reference when experimenting.

The offline verifier uses exact locked packages and a matching Windows CPython wheel folder. Python itself must already be installed. A fresh run creates the SQLite file locally; no original project environment or pre-existing database is needed.
