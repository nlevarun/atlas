"""Hiring Agent - Analyzes job postings for growth signals."""

from datetime import datetime, UTC
import asyncio
import uuid
import os
import sys
from typing import Optional
import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))

from schemas.evidence import Evidence, AgentReport
from .base import BaseAgent


class HiringAgent(BaseAgent):
    """Analyzes job postings to detect hiring trends and growth signals."""

    def __init__(self):
        """Initialize Hiring Agent."""
        pass

    @property
    def name(self) -> str:
        return "hiring_agent"

    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """
        Analyze job postings for hiring trends.

        Args:
            company_id: Company identifier
            run_id: Research run identifier

        Returns:
            AgentReport with hiring evidence
        """
        try:
            # Simulate job posting analysis
            # In real implementation, would scrape LinkedIn, Indeed, company careers page
            await asyncio.sleep(1)  # Simulate API call

            evidence_items = self._generate_hiring_evidence(company_id)
            summary = self._generate_summary(evidence_items, company_id)

            # Calculate hiring signals
            total_openings = len(evidence_items)
            roles_by_category = self._categorize_roles(evidence_items)

            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=evidence_items,
                summary=summary,
                signals={
                    "total_openings": total_openings,
                    "categories": roles_by_category,
                    "hiring_velocity": "high" if total_openings > 20 else "moderate",
                    "key_focus_areas": self._identify_focus_areas(roles_by_category),
                },
                status="ok",
                error=None
            )

        except Exception as e:
            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=[],
                summary=f"Failed to analyze hiring: {str(e)}",
                signals={},
                status="failed",
                error=str(e)
            )

    def _generate_hiring_evidence(self, company_id: str) -> list[Evidence]:
        """Generate evidence from job postings."""
        # Mock job posting data
        job_data = [
            {
                "title": "Senior Machine Learning Engineer",
                "count": 5,
                "description": "Building next-generation AI models for production systems. Focus on LLMs and reinforcement learning.",
                "category": "engineering"
            },
            {
                "title": "Product Manager - AI Platform",
                "count": 3,
                "description": "Leading product strategy for enterprise AI platform. Defining roadmap and customer requirements.",
                "category": "product"
            },
            {
                "title": "Enterprise Sales Executive",
                "count": 8,
                "description": "Driving revenue growth through enterprise customer acquisition. Experience with Fortune 500 required.",
                "category": "sales"
            },
            {
                "title": "Research Scientist - NLP",
                "count": 4,
                "description": "Advancing state-of-the-art in natural language understanding. Publishing in top-tier conferences.",
                "category": "research"
            },
            {
                "title": "Engineering Manager - Platform",
                "count": 2,
                "description": "Leading team building scalable infrastructure. Managing 10-15 engineers across backend and ML ops.",
                "category": "engineering"
            }
        ]

        evidence_items = []

        for job in job_data:
            claim = f"{company_id} is hiring {job['count']} {job['title']} position{'s' if job['count'] > 1 else ''}."

            evidence = Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim=claim,
                source_url=f"https://example.com/careers/{company_id.lower()}-{job['title'].lower().replace(' ', '-')}",
                source_type="job_posting",
                retrieved_at=datetime.now(UTC),
                confidence=0.88,
                raw_excerpt=f"Job posting: {job['title']}. {job['description']} Currently {job['count']} open positions."
            )
            evidence_items.append(evidence)

        return evidence_items

    def _categorize_roles(self, evidence: list[Evidence]) -> dict[str, int]:
        """Categorize roles by function."""
        categories = {}

        # Simple keyword-based categorization
        for item in evidence:
            claim = item.claim.lower()
            if "engineer" in claim or "technical" in claim:
                categories["engineering"] = categories.get("engineering", 0) + 1
            elif "sales" in claim or "business development" in claim:
                categories["sales"] = categories.get("sales", 0) + 1
            elif "product" in claim:
                categories["product"] = categories.get("product", 0) + 1
            elif "research" in claim or "scientist" in claim:
                categories["research"] = categories.get("research", 0) + 1
            else:
                categories["other"] = categories.get("other", 0) + 1

        return categories

    def _identify_focus_areas(self, categories: dict[str, int]) -> list[str]:
        """Identify key hiring focus areas."""
        # Sort by count and return top 3
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, _ in sorted_categories[:3]]

    def _generate_summary(self, evidence: list[Evidence], company_id: str) -> str:
        """Generate summary of hiring findings."""
        if not evidence:
            return f"No job postings found for {company_id}."

        total_positions = len(evidence)
        evidence_refs = ", ".join(e.id[:8] for e in evidence[:3])

        return (
            f"{company_id} has {total_positions} active job openings, indicating strong growth momentum. "
            f"Key hiring areas include engineering, sales, and product roles "
            f"(evidence: {evidence_refs})."
        )
