"""GET /api/portfolio/health: the Portfolio Health Score (methodology health-v2)."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter

from .. import schemas
from ..services import analysis_service
from ..services.presentation import public_health
from ..schemas.public import PublicHealth

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


@router.get("/health", response_model=PublicHealth)
def health(portfolio_id: Optional[str] = None):
    return public_health(analysis_service.analysis_for(portfolio_id)["health_score"])
