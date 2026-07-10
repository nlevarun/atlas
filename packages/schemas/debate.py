"""Debate schemas for multi-agent deliberation (Phase 3)."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class DebateTurn(BaseModel):
    """A single turn in a multi-agent debate."""

    turn_number: int
    agent: str
    stance: Literal["for", "against", "neutral"]
    argument: str
    evidence_ids: list[str]
    timestamp: datetime


class DebateResult(BaseModel):
    """Result of a multi-agent debate on a claim."""

    debate_id: str
    claim: str
    turns: list[DebateTurn]
    consensus_reached: bool
    final_verdict: Literal["supported", "refuted", "uncertain"]
    confidence: float
    summary: str
