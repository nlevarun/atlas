"""LangGraph state definition for research orchestration."""

from typing import TypedDict, Annotated
from datetime import datetime
import sys
import os

# Add schemas to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))

from schemas.evidence import AgentReport


def append_report(existing: list[AgentReport], new: AgentReport | list[AgentReport]) -> list[AgentReport]:
    """Append new reports to existing list."""
    if isinstance(new, list):
        return existing + new
    return existing + [new]


class ResearchState(TypedDict):
    """State for research orchestration workflow."""

    run_id: str
    company_id: str
    company_name: str
    started_at: datetime
    agent_reports: Annotated[list[AgentReport], append_report]
    status: str  # "started", "running_agents", "synthesizing", "completed", "failed"
    error: str | None
