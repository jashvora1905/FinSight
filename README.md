# FinSight - Portfolio Health Intelligence Platform

NMIMS MPSTME, B.Tech Computer Science and Business Systems, Year 3 Semester V. Review edition: 19 November 2026.

A working local portfolio-analysis prototype with deterministic analytics, risk/diversification, internal transaction diagnostics, aggregate health-v2 scoring, grounded offline insights and a local dashboard. The review adds reproducible historical backtests and full evidence artifacts. It does not establish predictive skill, commercial viability or regulatory approval.

## Run and independently verify
Windows PowerShell, from the extracted FinSight directory:

    powershell -ExecutionPolicy Bypass -File scripts/verify.ps1 -Offline -PythonVersion 3.12

Use PythonVersion 3.14 with the matching wheel folder if that is the installed Windows 64-bit interpreter. Python itself must already be installed. Offline wheels are in the pendrive package; GitHub contains the source, data, reports and results. For an online install, omit -Offline. For other operating systems use Python 3.12 or 3.14 in a virtual environment, install requirements-lock.txt, then run:

    python -m pytest -q
    python -m evaluation.run --verify
    python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

Open http://127.0.0.1:8000/app/ for the dashboard or /docs for the API. Upload data/sample_portfolio.csv and optionally data/sample_transactions.csv. Their role is synthetic demonstration data, not broker-account history. Market prices are separately frozen in data/market/.

## Evidence
- docs/reports/: three revised progress reports, architecture, audit and backtesting/commercial notes.
- docs/file_inventory.json: every production Python file, purpose, imports, functions and hash.
- results/: 120 market runs, trade ledgers, daily curves, 152 pipeline checkpoints, sample analysis, test evidence and expected.json.gz.
- data/market/provenance.json: raw-response URLs and checksums. No download is required for evaluation.
- scripts/verify.ps1 and requirements-lock.txt: clean-install and reproduction path.

The original archive passes 312 tests plus 20 subtests in this audit. The refined suite passes 359 tests plus 20 subtests on Windows Python 3.12 and 3.14 with pandas 2.3.3. The previous 338-test statement was not reproducible from the ZIP. No live AI model or pandas 3 validation is claimed. See saved test logs for the precise environment and dependency warnings.

## Honest results and limits
The fixed SMA50 research strategy underperformed same-series buy-and-hold on all five series in 2023-2025 at 10 bps per side. The synthetic sample's four matched sale transactions have a 25% win rate and negative realised P&L. This is distinct from positive unrealised snapshot performance. Do not combine those denominators or describe research strategy results as FinSight predictions.

Public API responses omit detailed behaviour and health component diagnostics. Internal evaluator artifacts are marked internal. This is a single-user localhost prototype with no authentication, broker integration, live market feed or order execution. Heuristic scores are not validated forecasts or suitability measures. No current regulatory-compliance claim is made.

## Team and fair review allocation
Rayyan Chunawala E014; Ricky Maishari E037; Prisha Mistry E042; Soumil Patro E050; Aditya Shah E062; Atharva Suryavanshi E065; Jash Vora E067. docs/contributions.md assigns seven equally weighted review packages. It is a plan for member verification, not an invented record of historical effort or authorship.
