"""Company profile schemas for Atlas."""

from datetime import datetime
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .evidence import AgentReport


class NarrativeSection(BaseModel):
    """A section of the company narrative with evidence citations."""

    heading: str
    bullets: list[str]
    evidence_ids: list[str]


class CompanyProfile(BaseModel):
    """Complete company dossier with narrative and agent reports."""

    company_id: str
    name: str
    ticker: str | None
    website: str | None
    last_updated: datetime
    current_strategy: NarrativeSection
    growth_signals: NarrativeSection
    risks: NarrativeSection
    agent_reports: list[dict]  # Will be AgentReport once imported
