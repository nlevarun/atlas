"""Evidence and Agent Report schemas for Atlas."""

from datetime import datetime
from typing import Literal, Any
from pydantic import BaseModel, HttpUrl, Field
import uuid


class Evidence(BaseModel):
    """Atomic piece of evidence with source attribution."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent: str                    # e.g. "hiring_agent"
    claim: str                    # Atomic fact, one sentence
    source_url: HttpUrl | None
    source_type: Literal[
        "sec_filing", "news", "github", "job_posting", "patent",
        "social", "website_diff", "review", "pricing_page",
        "legal_filing", "press_release", "market_report", "demo_data"
    ]
    retrieved_at: datetime
    confidence: float = Field(ge=0.0, le=1.0)
    raw_excerpt: str              # Verbatim snippet from source


class AgentReport(BaseModel):
    """Report from a single agent after research completion."""

    agent: str
    company_id: str
    run_id: str
    evidence: list[Evidence]
    summary: str                  # 2-3 sentences, references evidence ids
    signals: dict[str, Any]       # Agent-specific structured fields
    status: Literal["ok", "partial", "failed"]
    error: str | None = None
