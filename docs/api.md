# Public API - review edition
Run from the repository root: python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000. Interactive schemas are at /docs; the local dashboard is /app/.

POST /api/portfolio/upload accepts multipart portfolio (required CSV), transactions (optional CSV), price_history (optional date,symbol,close CSV), portfolio_id and ISO observation_start/observation_end. Per-file limit: 5 MB. UTF-8 with optional BOM. Invalid data returns a detail field and a suitable 4xx status; unexpected errors return generic 500.

The public upload envelope is portfolio_id, portfolio_ids, inputs, analytics, risk, health_score. Public health contains score, band, score_basis, methodology_version and limitations. It never contains behaviour diagnostics, component scores, drivers or missing-component names. Internal health-v2 calculation and weights remain unchanged. GET /api/portfolio/behavior is removed and absent from OpenAPI.

GET /api/portfolio/{summary,holdings,performance,allocation,risk,diversification,health,insights} accepts optional portfolio_id. Without it, analysis uses the most recent upload scope. Before upload or for an unknown portfolio, return 404. Multi-portfolio transactions require explicit portfolio selection. Re-upload replaces existing data for affected portfolios; invalid uploads write nothing.

Insights return status, source, methodology_version, summary, insights, areas_to_review, limitations and disclaimer. Each insight contains id, category, text and evidence path/value pairs. The implementation is deterministic offline; selector tests are not a live-provider integration. Public endpoints are a local single-user demonstration, not a multiuser service.

Breaking changes from the ZIP: 501 insights becomes a grounded working endpoint; private behaviour routing is removed; public upload/health schemas omit internal diagnostics. Internal engine APIs remain available to the test/research harness.
