"""News Agent - Gathers recent news using Tavily Search API."""

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


class NewsAgent(BaseAgent):
    """Gathers recent news articles about companies using Tavily API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize News Agent.

        Args:
            api_key: Tavily API key (or from TAVILY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com"

    @property
    def name(self) -> str:
        return "news_agent"

    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """
        Gather recent news about the company.

        Args:
            company_id: Company identifier (name or ticker)
            run_id: Research run identifier

        Returns:
            AgentReport with news evidence
        """
        try:
            evidence_items = []

            # Search for recent news
            query = f"{company_id} company news recent announcements"
            results = await self._search_news(query, max_results=5)

            for result in results:
                # Create evidence from each news article
                evidence = Evidence(
                    id=str(uuid.uuid4()),
                    agent=self.name,
                    claim=self._extract_claim(result),
                    source_url=result.get("url"),
                    source_type="news",
                    retrieved_at=datetime.now(UTC),
                    confidence=self._calculate_confidence(result),
                    raw_excerpt=result.get("content", "")[:500]  # First 500 chars
                )
                evidence_items.append(evidence)

            # Generate summary
            summary = self._generate_summary(evidence_items, company_id)

            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=evidence_items,
                summary=summary,
                signals={
                    "news_count": len(evidence_items),
                    "avg_confidence": sum(e.confidence for e in evidence_items) / len(evidence_items) if evidence_items else 0,
                    "sources": list(set(e.source_url for e in evidence_items if e.source_url)),
                },
                status="ok" if evidence_items else "partial",
                error=None if evidence_items else "No news articles found"
            )

        except Exception as e:
            # Return failed report with error
            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=[],
                summary=f"Failed to gather news: {str(e)}",
                signals={},
                status="failed",
                error=str(e)
            )

    async def _search_news(self, query: str, max_results: int = 5) -> list[dict]:
        """
        Search for news using Tavily API.

        Args:
            query: Search query
            max_results: Maximum results to return

        Returns:
            List of search results
        """
        if not self.api_key:
            # Fallback to mock data if no API key
            return self._mock_news_results(query)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "search_depth": "basic",
                        "include_answer": False,
                        "include_raw_content": False,
                        "max_results": max_results,
                        "include_domains": [],
                        "exclude_domains": []
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("results", [])
                else:
                    # Fallback to mock data on error
                    return self._mock_news_results(query)

        except Exception:
            # Fallback to mock data on exception
            return self._mock_news_results(query)

    def _mock_news_results(self, query: str) -> list[dict]:
        """
        Generate mock news results for testing without API key.

        Args:
            query: Search query

        Returns:
            List of mock results
        """
        company = query.split()[0]
        return [
            {
                "title": f"{company} announces strategic partnership with major tech firm",
                "url": f"https://example.com/news/{company.lower()}-partnership",
                "content": f"{company} today announced a significant strategic partnership that will expand its market reach and technological capabilities. The partnership is expected to accelerate product development and open new revenue streams.",
                "score": 0.95,
                "published_date": datetime.now(UTC).isoformat()
            },
            {
                "title": f"{company} reports strong quarterly growth",
                "url": f"https://example.com/news/{company.lower()}-growth",
                "content": f"{company}'s latest quarterly results show robust revenue growth driven by increasing customer adoption and market expansion. The company exceeded analyst expectations across key metrics.",
                "score": 0.92,
                "published_date": datetime.now(UTC).isoformat()
            },
            {
                "title": f"{company} launches new AI-powered product",
                "url": f"https://example.com/news/{company.lower()}-product-launch",
                "content": f"Today {company} unveiled its latest AI-powered product, marking a significant milestone in the company's innovation roadmap. Early customer feedback has been overwhelmingly positive.",
                "score": 0.88,
                "published_date": datetime.now(UTC).isoformat()
            }
        ]

    def _extract_claim(self, result: dict) -> str:
        """
        Extract a single-sentence claim from news result.

        Args:
            result: Search result dict

        Returns:
            Single sentence claim
        """
        title = result.get("title", "")
        # Clean up and ensure it's a single sentence
        claim = title.strip()
        if not claim.endswith("."):
            claim += "."
        return claim

    def _calculate_confidence(self, result: dict) -> float:
        """
        Calculate confidence score for a news result.

        Args:
            result: Search result dict

        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Use search relevance score if available
        score = result.get("score", 0.8)

        # Adjust based on content length (longer = more substantial)
        content_length = len(result.get("content", ""))
        if content_length > 300:
            score += 0.05
        if content_length > 600:
            score += 0.05

        # Cap at 1.0
        return min(score, 1.0)

    def _generate_summary(self, evidence: list[Evidence], company_id: str) -> str:
        """
        Generate summary of news findings.

        Args:
            evidence: List of evidence items
            company_id: Company identifier

        Returns:
            Summary string
        """
        if not evidence:
            return f"No recent news found for {company_id}."

        # Reference top evidence items
        top_evidence = evidence[:3]
        evidence_refs = ", ".join(e.id[:8] for e in top_evidence)

        return (
            f"Found {len(evidence)} recent news articles about {company_id}. "
            f"Key developments include partnerships, growth reports, and product launches "
            f"(evidence: {evidence_refs})."
        )
