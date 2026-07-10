"""Dummy agent for Phase 0 pipeline validation."""

from datetime import datetime, UTC
import asyncio
import uuid
import sys
import os

# Add schemas to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))

from schemas.evidence import Evidence, AgentReport
from .base import BaseAgent


class DummyAgent(BaseAgent):
    """Phase 0 dummy agent - returns hardcoded evidence to prove the pipeline."""

    @property
    def name(self) -> str:
        return "dummy_agent"

    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """Return hardcoded evidence for pipeline testing."""
        # Simulate research delay
        await asyncio.sleep(2)

        evidence = [
            Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim="Company announced Q4 2025 earnings beat expectations",
                source_url="https://example.com/press-release",
                source_type="demo_data",
                retrieved_at=datetime.now(UTC),
                confidence=0.95,
                raw_excerpt="Q4 2025 revenue increased 25% YoY to $1.2B, exceeding analyst estimates of $1.1B. Net income rose to $180M from $120M in Q4 2024."
            ),
            Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim="Expanded engineering team by 50 employees in past quarter",
                source_url="https://example.com/careers",
                source_type="demo_data",
                retrieved_at=datetime.now(UTC),
                confidence=0.85,
                raw_excerpt="Join our growing team of 200+ engineers building the future of AI. We've expanded rapidly, adding 50 new positions across backend, ML, and infrastructure teams this quarter."
            ),
            Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim="Launched new AI product feature in European market",
                source_url="https://example.com/blog/eu-launch",
                source_type="demo_data",
                retrieved_at=datetime.now(UTC),
                confidence=0.90,
                raw_excerpt="Today we're thrilled to announce the launch of our advanced AI analytics suite across the European Union, bringing intelligent insights to over 10,000 new customers."
            )
        ]

        return AgentReport(
            agent=self.name,
            company_id=company_id,
            run_id=run_id,
            evidence=evidence,
            summary=f"Dummy agent found 3 key signals for {company_id}: strong earnings performance (evidence {evidence[0].id[:8]}), rapid team expansion (evidence {evidence[1].id[:8]}), and European market entry (evidence {evidence[2].id[:8]}).",
            signals={
                "dummy_metric": 42,
                "evidence_count": len(evidence),
                "avg_confidence": sum(e.confidence for e in evidence) / len(evidence)
            },
            status="ok"
        )
