"""Grounded offline explanations; an optional selector reorders approved facts only.

Provider prose is never accepted. No live model/network client is configured.
"""
from copy import deepcopy

DISCLAIMER = "Informational academic prototype. Not personalised investment advice or a forecast."


def generate_insights(public, *, selector=None, prioritize_risk=False):
    health, analytics, risk = public["health_score"], public["analytics"], public["risk"]
    def item(key, category, text, path, value):
        return {"id": key, "category": category, "text": text,
                "evidence": [{"path": path, "value": value}]}
    facts = [
        item("health", "health", f"The aggregate health score is {health['score']:.2f} ({health['band']}).",
             "health_score.score", health["score"]),
        item("concentration", "risk", f"The largest holding represents {risk['concentration']['largest_holding_pct']:.2f}% of current portfolio value.",
             "risk.concentration.largest_holding_pct", risk["concentration"]["largest_holding_pct"]),
        item("diversification", "diversification", f"The prototype diversification score is {risk['diversification']['diversification_score']:.2f} out of 100.",
             "risk.diversification.diversification_score", risk["diversification"]["diversification_score"]),
    ]
    ret = analytics["summary"].get("return_pct")
    if ret is not None:
        facts.append(item("performance", "performance", f"The snapshot return since the supplied purchase cost is {ret:.2f}%; this is not an annualised return.",
                          "analytics.summary.return_pct", ret))
    if prioritize_risk:
        facts.sort(key=lambda f: f["category"] != "risk")
    source = "deterministic"
    if selector is not None:
        try:
            ids = selector(deepcopy(facts))
            allowed = {f["id"]: f for f in facts}
            if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
                raise ValueError("Invalid selector output")
            if len(ids) != len(allowed) or set(ids) != set(allowed):
                raise ValueError("Selector must return every approved ID exactly once")
            facts = [allowed[i] for i in ids]
            source = "validated_selector"
        except Exception:
            source = "deterministic_fallback"
    limitations = ["Portfolio calculations use supplied prices; they are not live quotes.",
                   "The diversification model does not look through funds or ETFs."] + list(health["limitations"])
    if not risk["risk_metrics"]["historical_data_available"]:
        limitations.append("Historical volatility and drawdown are unavailable for this portfolio.")
    return {"status": "ok", "source": source, "methodology_version": "grounded-insights-v1",
            "summary": "Portfolio observations grounded in the supplied data.", "insights": facts,
            "areas_to_review": [deepcopy(f) for f in facts if f["category"] in {"risk", "diversification"}],
            "limitations": limitations, "disclaimer": DISCLAIMER}
