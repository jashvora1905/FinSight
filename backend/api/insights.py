"""Public grounded explanations. Private diagnostics remain Python-only."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter

from ai import generate_insights
from ..services.analysis_service import analysis_for
from ..services.presentation import public_health
from ..services.joint_context import combined_context

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


@router.get("/insights")
def insights(portfolio_id: Optional[str] = None):
    internal = analysis_for(portfolio_id)
    context = combined_context(internal["risk"], internal["behavior"])
    public = {"analytics": internal["analytics"], "risk": internal["risk"],
              "health_score": public_health(internal["health_score"])}
    return generate_insights(public, prioritize_risk=context["priority"] == "enhanced")
