"""Public schema intentionally omits private diagnostic components."""
from typing import List, Optional
from pydantic import BaseModel
from .portfolio import Analytics
from .risk import Risk
from .common import UploadInputs


class PublicHealth(BaseModel):
    score: float
    band: str
    score_basis: str
    methodology_version: str
    limitations: List[str]


class PublicUpload(BaseModel):
    portfolio_id: Optional[str] = None
    portfolio_ids: List[str]
    inputs: UploadInputs
    analytics: Analytics
    risk: Risk
    health_score: PublicHealth
