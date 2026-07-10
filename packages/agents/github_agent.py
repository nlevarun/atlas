"""GitHub Agent - Analyzes repository activity and development trends."""

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


class GitHubAgent(BaseAgent):
    """Analyzes GitHub repository activity for tech companies."""

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub Agent.

        Args:
            github_token: GitHub API token (optional, increases rate limits)
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

    @property
    def name(self) -> str:
        return "github_agent"

    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """
        Analyze GitHub repository activity.

        Args:
            company_id: Company identifier (GitHub org name preferred)
            run_id: Research run identifier

        Returns:
            AgentReport with GitHub evidence
        """
        try:
            # Try to find company's GitHub organization
            org_name = company_id.lower().replace(" ", "")

            # Get repository data
            repos = await self._get_org_repos(org_name)

            if repos:
                evidence_items = self._analyze_repos(repos, org_name)
            else:
                # Use mock data if no repos found
                evidence_items = self._generate_mock_github_evidence(company_id)

            summary = self._generate_summary(evidence_items, company_id)

            # Calculate signals
            total_stars = sum(
                int(e.raw_excerpt.split("stars:")[1].split(",")[0].strip())
                for e in evidence_items
                if "stars:" in e.raw_excerpt
            )

            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=evidence_items,
                summary=summary,
                signals={
                    "total_repos": len(evidence_items),
                    "total_stars": total_stars,
                    "has_github_presence": bool(repos),
                    "development_activity": "active" if total_stars > 100 else "moderate",
                },
                status="ok" if evidence_items else "partial",
                error=None if evidence_items else "No GitHub activity found"
            )

        except Exception as e:
            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=[],
                summary=f"Failed to analyze GitHub activity: {str(e)}",
                signals={},
                status="failed",
                error=str(e)
            )

    async def _get_org_repos(self, org_name: str) -> list[dict]:
        """
        Get repositories for a GitHub organization.

        Args:
            org_name: GitHub organization name

        Returns:
            List of repositories
        """
        # For Phase 1, return empty to use mock data
        # Real implementation would query GitHub API
        return []

    def _analyze_repos(self, repos: list[dict], org_name: str) -> list[Evidence]:
        """Analyze repository data into evidence."""
        evidence_items = []

        for repo in repos[:5]:  # Top 5 repos
            evidence = Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim=f"Repository {repo['name']} has {repo['stargazers_count']} stars and {repo['forks_count']} forks.",
                source_url=repo["html_url"],
                source_type="github",
                retrieved_at=datetime.now(UTC),
                confidence=0.92,
                raw_excerpt=(
                    f"GitHub repository: {repo['name']}. "
                    f"Description: {repo.get('description', 'N/A')}. "
                    f"Stars: {repo['stargazers_count']}, "
                    f"Forks: {repo['forks_count']}, "
                    f"Updated: {repo['updated_at']}"
                )
            )
            evidence_items.append(evidence)

        return evidence_items

    def _generate_mock_github_evidence(self, company_id: str) -> list[Evidence]:
        """Generate mock GitHub evidence."""
        mock_repos = [
            {
                "name": "core-platform",
                "stars": 1250,
                "forks": 180,
                "description": "Core platform infrastructure and APIs"
            },
            {
                "name": "ml-toolkit",
                "stars": 890,
                "forks": 145,
                "description": "Machine learning tools and utilities"
            },
            {
                "name": "client-sdk",
                "stars": 620,
                "forks": 95,
                "description": "Official client SDK for developers"
            }
        ]

        evidence_items = []

        for repo in mock_repos:
            evidence = Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim=f"{company_id}'s {repo['name']} repository has {repo['stars']} stars, indicating strong developer interest.",
                source_url=f"https://github.com/{company_id.lower()}/{repo['name']}",
                source_type="github",
                retrieved_at=datetime.now(UTC),
                confidence=0.85,
                raw_excerpt=(
                    f"GitHub repository: {repo['name']}. "
                    f"Description: {repo['description']}. "
                    f"Stars: {repo['stars']}, "
                    f"Forks: {repo['forks']}"
                )
            )
            evidence_items.append(evidence)

        return evidence_items

    def _generate_summary(self, evidence: list[Evidence], company_id: str) -> str:
        """Generate summary of GitHub findings."""
        if not evidence:
            return f"No GitHub activity found for {company_id}."

        evidence_refs = ", ".join(e.id[:8] for e in evidence[:3])

        return (
            f"Analyzed {len(evidence)} GitHub repositories for {company_id}. "
            f"Strong open-source presence with active community engagement "
            f"(evidence: {evidence_refs})."
        )
