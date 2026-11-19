"""Explicit public allowlists. Internal diagnostics never cross this boundary."""
from copy import deepcopy


def public_health(result):
    return {"score": result["score"], "band": result["band"],
            "score_basis": result["score_basis"], "methodology_version": result["methodology_version"],
            "limitations": ["Experimental composite score; not a forecast or investor-skill measure."] +
            (["Some inputs are unavailable; this aggregate score is provisional."] if result["score_basis"] == "partial" else [])}


def public_upload(result):
    return {"portfolio_id": result["portfolio_id"], "portfolio_ids": list(result["portfolio_ids"]),
            "inputs": deepcopy(result["inputs"]), "analytics": deepcopy(result["analytics"]),
            "risk": deepcopy(result["risk"]), "health_score": public_health(result["health_score"])}
