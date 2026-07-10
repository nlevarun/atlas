"""LangGraph orchestration graph for research workflow."""

import asyncio
from datetime import datetime, UTC
from typing import Any
import sys
import os

# Add packages to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'synthesis'))

from agents.dummy import DummyAgent
from agents.news_agent import NewsAgent
from agents.financial_agent import FinancialAgent
from agents.hiring_agent import HiringAgent
from agents.github_agent import GitHubAgent
from synthesis import EvidenceSynthesizer
from .state import ResearchState


class ResearchOrchestrator:
    """Orchestrates research workflow with fan-out/fan-in pattern."""

    def __init__(self, websocket_manager: Any = None, use_real_agents: bool = True):
        """
        Initialize orchestrator.

        Args:
            websocket_manager: Optional WebSocket manager for streaming events
            use_real_agents: Use real agents (Phase 1) or dummy agent (Phase 0)
        """
        self.websocket_manager = websocket_manager

        # Initialize synthesizer (template-based by default, free!)
        use_groq = os.getenv("USE_GROQ_SYNTHESIS", "false").lower() == "true"
        self.synthesizer = EvidenceSynthesizer(use_groq=use_groq)

        if use_real_agents:
            # Phase 1: Real agents
            self.agents = [
                NewsAgent(),
                FinancialAgent(),
                HiringAgent(),
                GitHubAgent(),
            ]
        else:
            # Phase 0: Dummy agent only
            self.agents = [DummyAgent()]

    async def _broadcast_event(self, run_id: str, event: dict):
        """Broadcast event to WebSocket clients."""
        if self.websocket_manager:
            await self.websocket_manager.broadcast(run_id, event)

    async def execute(self, state: ResearchState) -> ResearchState:
        """
        Execute full research workflow.

        Args:
            state: Initial research state

        Returns:
            Updated state after completion
        """
        # Start node
        state = await self._start_node(state)

        # Run agents node
        state = await self._run_agents_node(state)

        # Synthesize node
        state = await self._synthesize_node(state)

        return state

    async def _start_node(self, state: ResearchState) -> ResearchState:
        """Initialize research run."""
        state["status"] = "started"
        state["started_at"] = datetime.now(UTC)

        # Broadcast start event
        await self._broadcast_event(state["run_id"], {
            "type": "run_started",
            "run_id": state["run_id"],
            "company_name": state["company_name"],
            "timestamp": state["started_at"].isoformat()
        })

        return state

    async def _run_agents_node(self, state: ResearchState) -> ResearchState:
        """Fan out to agents in parallel."""
        state["status"] = "running_agents"

        # Broadcast agent start
        await self._broadcast_event(state["run_id"], {
            "type": "agents_started",
            "agent_count": len(self.agents),
            "timestamp": datetime.now(UTC).isoformat()
        })

        # Execute agents in parallel (Phase 0: just one agent)
        tasks = []
        for agent in self.agents:
            # Broadcast individual agent start
            await self._broadcast_event(state["run_id"], {
                "type": "agent_started",
                "agent": agent.name,
                "timestamp": datetime.now(UTC).isoformat()
            })
            tasks.append(agent.execute(state["company_id"], state["run_id"]))

        # Wait for all agents to complete
        reports = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for i, result in enumerate(reports):
            agent_name = self.agents[i].name

            if isinstance(result, Exception):
                # Agent failed
                await self._broadcast_event(state["run_id"], {
                    "type": "agent_failed",
                    "agent": agent_name,
                    "error": str(result),
                    "timestamp": datetime.now(UTC).isoformat()
                })
            else:
                # Agent succeeded
                state["agent_reports"].append(result)

                # Broadcast agent completion
                await self._broadcast_event(state["run_id"], {
                    "type": "agent_completed",
                    "agent": agent_name,
                    "evidence_count": len(result.evidence),
                    "status": result.status,
                    "timestamp": datetime.now(UTC).isoformat()
                })

                # Broadcast individual evidence items
                for evidence in result.evidence:
                    await self._broadcast_event(state["run_id"], {
                        "type": "evidence_found",
                        "agent": agent_name,
                        "claim": evidence.claim,
                        "confidence": evidence.confidence,
                        "source_type": evidence.source_type,
                        "timestamp": datetime.now(UTC).isoformat()
                    })

        return state

    async def _synthesize_node(self, state: ResearchState) -> ResearchState:
        """Synthesize agent reports into narrative."""
        state["status"] = "synthesizing"

        await self._broadcast_event(state["run_id"], {
            "type": "synthesis_started",
            "timestamp": datetime.now(UTC).isoformat()
        })

        try:
            # Run synthesis
            profile = await self.synthesizer.synthesize(
                company_id=state["company_id"],
                company_name=state["company_name"],
                agent_reports=state["agent_reports"]
            )

            # Store profile in state (for Phase 1+ when we have Postgres)
            # For now, just log that synthesis completed
            state["status"] = "completed"

            await self._broadcast_event(state["run_id"], {
                "type": "synthesis_completed",
                "sections": {
                    "strategy": len(profile.current_strategy.bullets),
                    "growth": len(profile.growth_signals.bullets),
                    "risks": len(profile.risks.bullets)
                },
                "timestamp": datetime.now(UTC).isoformat()
            })

        except Exception as e:
            state["status"] = "completed"  # Still mark complete even if synthesis fails
            await self._broadcast_event(state["run_id"], {
                "type": "synthesis_failed",
                "error": str(e),
                "timestamp": datetime.now(UTC).isoformat()
            })

        await self._broadcast_event(state["run_id"], {
            "type": "run_completed",
            "run_id": state["run_id"],
            "total_evidence": sum(len(r.evidence) for r in state["agent_reports"]),
            "timestamp": datetime.now(UTC).isoformat()
        })

        return state
