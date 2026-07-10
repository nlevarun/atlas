"""Research API endpoints."""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from datetime import datetime, UTC
import uuid
import sys
import os
import asyncio

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'packages', 'orchestrator'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'packages', 'schemas'))

from orchestrator import ResearchOrchestrator, ResearchState
from routers.websocket import manager
from routers.config import USE_REAL_AGENTS

router = APIRouter()

# In-memory storage for Phase 0 (will be Postgres in Phase 1)
research_runs = {}


class ResearchRequest(BaseModel):
    """Request to start company research."""
    company_name: str
    ticker: str | None = None


class ResearchResponse(BaseModel):
    """Response with run ID."""
    run_id: str
    status: str


class RunStatus(BaseModel):
    """Status of a research run."""
    run_id: str
    company_name: str
    status: str
    started_at: datetime
    agent_count: int
    evidence_count: int


@router.post("/company", response_model=ResearchResponse)
async def start_company_research(
    req: ResearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new company research run.

    This endpoint initiates research orchestration and returns immediately.
    Use WebSocket to receive live updates, or poll /status endpoint.
    """
    run_id = str(uuid.uuid4())
    company_id = req.ticker or req.company_name.lower().replace(" ", "_")

    # Initialize state
    initial_state: ResearchState = {
        "run_id": run_id,
        "company_id": company_id,
        "company_name": req.company_name,
        "started_at": datetime.now(UTC),
        "agent_reports": [],
        "status": "pending",
        "error": None
    }

    research_runs[run_id] = initial_state

    # Start research in background
    background_tasks.add_task(run_research, run_id, initial_state)

    return ResearchResponse(
        run_id=run_id,
        status="started"
    )


async def run_research(run_id: str, state: ResearchState):
    """Execute research orchestration."""
    try:
        orchestrator = ResearchOrchestrator(
            websocket_manager=manager,
            use_real_agents=USE_REAL_AGENTS
        )
        final_state = await orchestrator.execute(state)

        # Update stored state
        research_runs[run_id] = final_state

    except Exception as e:
        # Update state with error
        state["status"] = "failed"
        state["error"] = str(e)
        research_runs[run_id] = state

        # Broadcast error
        await manager.broadcast(run_id, {
            "type": "run_failed",
            "run_id": run_id,
            "error": str(e),
            "timestamp": datetime.now(UTC).isoformat()
        })


@router.get("/{run_id}/status", response_model=RunStatus)
async def get_research_status(run_id: str):
    """
    Get status of a research run.

    Returns current progress and agent completion status.
    """
    if run_id not in research_runs:
        raise HTTPException(status_code=404, detail="Run not found")

    state = research_runs[run_id]

    return RunStatus(
        run_id=run_id,
        company_name=state["company_name"],
        status=state["status"],
        started_at=state["started_at"],
        agent_count=len(state["agent_reports"]),
        evidence_count=sum(len(r.evidence) for r in state["agent_reports"])
    )


@router.get("/{run_id}/report")
async def get_research_report(run_id: str):
    """
    Get full research report with all evidence.

    Returns the complete dossier once synthesis is complete.
    """
    if run_id not in research_runs:
        raise HTTPException(status_code=404, detail="Run not found")

    state = research_runs[run_id]

    if state["status"] not in ["completed", "failed"]:
        return {
            "run_id": run_id,
            "status": state["status"],
            "message": "Research still in progress"
        }

    # Compile report
    report = {
        "run_id": run_id,
        "company_id": state["company_id"],
        "company_name": state["company_name"],
        "status": state["status"],
        "started_at": state["started_at"].isoformat(),
        "agent_reports": [
            {
                "agent": r.agent,
                "status": r.status,
                "summary": r.summary,
                "evidence_count": len(r.evidence),
                "evidence": [
                    {
                        "id": e.id,
                        "claim": e.claim,
                        "source_url": str(e.source_url) if e.source_url else None,
                        "source_type": e.source_type,
                        "confidence": e.confidence,
                        "raw_excerpt": e.raw_excerpt,
                        "retrieved_at": e.retrieved_at.isoformat()
                    }
                    for e in r.evidence
                ]
            }
            for r in state["agent_reports"]
        ],
        "total_evidence": sum(len(r.evidence) for r in state["agent_reports"])
    }

    return report


@router.get("/runs", response_model=list[RunStatus])
async def list_research_runs():
    """List all research runs."""
    return [
        RunStatus(
            run_id=run_id,
            company_name=state["company_name"],
            status=state["status"],
            started_at=state["started_at"],
            agent_count=len(state["agent_reports"]),
            evidence_count=sum(len(r.evidence) for r in state["agent_reports"])
        )
        for run_id, state in research_runs.items()
    ]
