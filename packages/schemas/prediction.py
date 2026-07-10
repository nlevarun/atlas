"""Prediction schemas for forecasting (Phase 4)."""

from datetime import datetime
from pydantic import BaseModel, Field


class Prediction(BaseModel):
    """A forecasted outcome with confidence and reasoning."""

    prediction_id: str
    company_id: str
    question: str
    prediction: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    evidence_ids: list[str]
    created_at: datetime
    resolve_by: datetime
    resolved: bool = False
    actual_outcome: str | None = None
