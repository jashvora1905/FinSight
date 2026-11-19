"""Internal prioritisation only. Never changes health-v2 or produces public text."""


def combined_context(risk, behavior):
    c = risk["concentration"]
    exposure = c["largest_holding_pct"] >= 40 or c["largest_sector_pct"] >= 60
    score = (behavior or {}).get("behavior_score", {})
    available = score.get("status") == "available" and score.get("value") is not None
    concern = 100 - score["value"] if available else None
    enhanced = exposure and available and concern >= 25
    return {"methodology_version": "joint-review-v1", "exposure_flag": exposure,
            "behavior_available": available, "concern": concern,
            "priority": "enhanced" if enhanced else "exposure" if exposure else "normal",
            "limitation": "Internal prototype triage thresholds; no extra numerical score penalty."}
