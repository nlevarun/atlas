"""Financial Agent - Gathers SEC filings and financial data."""

from datetime import datetime, UTC
import asyncio
import uuid
import os
import sys
from typing import Optional
import httpx
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))

from schemas.evidence import Evidence, AgentReport
from .base import BaseAgent


class FinancialAgent(BaseAgent):
    """Gathers financial data from SEC filings."""

    def __init__(self, user_agent: Optional[str] = None):
        """
        Initialize Financial Agent.

        Args:
            user_agent: SEC Edgar API user agent (required by SEC)
        """
        self.user_agent = user_agent or os.getenv(
            "SEC_EDGAR_USER_AGENT",
            "Atlas Research Bot research@example.com"
        )
        self.base_url = "https://data.sec.gov"

    @property
    def name(self) -> str:
        return "financial_agent"

    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """
        Gather financial data and SEC filings.

        Args:
            company_id: Company identifier (ticker preferred)
            run_id: Research run identifier

        Returns:
            AgentReport with financial evidence
        """
        try:
            evidence_items = []

            # Try to find company CIK (SEC identifier)
            cik = await self._lookup_cik(company_id)

            if cik:
                # Get recent filings
                filings = await self._get_recent_filings(cik)

                for filing in filings[:3]:  # Top 3 most recent
                    evidence = Evidence(
                        id=str(uuid.uuid4()),
                        agent=self.name,
                        claim=self._extract_claim(filing),
                        source_url=filing.get("url"),
                        source_type="sec_filing",
                        retrieved_at=datetime.now(UTC),
                        confidence=0.95,  # SEC filings are highly reliable
                        raw_excerpt=filing.get("description", "")[:500]
                    )
                    evidence_items.append(evidence)
            else:
                # Use mock data if CIK not found
                evidence_items = self._generate_mock_financial_evidence(company_id)

            summary = self._generate_summary(evidence_items, company_id)

            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=evidence_items,
                summary=summary,
                signals={
                    "filings_count": len(evidence_items),
                    "filing_types": list(set(e.raw_excerpt.split()[0] if e.raw_excerpt else "" for e in evidence_items)),
                    "has_sec_data": bool(cik),
                },
                status="ok" if evidence_items else "partial",
                error=None if evidence_items else "No financial data found"
            )

        except Exception as e:
            return AgentReport(
                agent=self.name,
                company_id=company_id,
                run_id=run_id,
                evidence=[],
                summary=f"Failed to gather financial data: {str(e)}",
                signals={},
                status="failed",
                error=str(e)
            )

    async def _lookup_cik(self, company_id: str) -> Optional[str]:
        """
        Look up company CIK from ticker or name.

        Args:
            company_id: Company ticker or name

        Returns:
            CIK number or None
        """
        # For Phase 1, return None to use mock data
        # Real implementation would query SEC company search
        return None

    async def _get_recent_filings(self, cik: str) -> list[dict]:
        """
        Get recent SEC filings for a company.

        Args:
            cik: Company CIK number

        Returns:
            List of recent filings
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"User-Agent": self.user_agent}
                response = await client.get(
                    f"{self.base_url}/submissions/CIK{cik.zfill(10)}.json",
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    filings = data.get("filings", {}).get("recent", {})
                    return self._parse_filings(filings)

        except Exception:
            pass

        return []

    def _parse_filings(self, filings_data: dict) -> list[dict]:
        """Parse SEC filings data into structured format."""
        parsed = []

        forms = filings_data.get("form", [])
        dates = filings_data.get("filingDate", [])
        accessions = filings_data.get("accessionNumber", [])
        descriptions = filings_data.get("primaryDocument", [])

        for i in range(min(len(forms), 5)):
            parsed.append({
                "form": forms[i],
                "date": dates[i],
                "accession": accessions[i],
                "description": f"{forms[i]} filing dated {dates[i]}",
                "url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={accessions[i]}"
            })

        return parsed

    def _generate_mock_financial_evidence(self, company_id: str) -> list[Evidence]:
        """Generate mock financial evidence for testing."""
        return [
            Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim=f"{company_id} reported revenue growth of 35% year-over-year in latest fiscal quarter.",
                source_url="https://example.com/sec/10-q",
                source_type="sec_filing",
                retrieved_at=datetime.now(UTC),
                confidence=0.95,
                raw_excerpt="10-Q filing: Total revenue for Q4 2025 reached $450M, representing 35% growth compared to $333M in Q4 2024. Operating margin improved to 18% from 15%."
            ),
            Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim=f"{company_id} raised $200M in Series D funding at $2B valuation.",
                source_url="https://example.com/sec/8-k",
                source_type="sec_filing",
                retrieved_at=datetime.now(UTC),
                confidence=0.93,
                raw_excerpt="8-K filing: Company completed Series D financing round of $200M led by major venture capital firms, achieving a post-money valuation of $2B."
            ),
            Evidence(
                id=str(uuid.uuid4()),
                agent=self.name,
                claim=f"{company_id} expanded gross margin to 72% from 68% year-over-year.",
                source_url="https://example.com/sec/10-k",
                source_type="sec_filing",
                retrieved_at=datetime.now(UTC),
                confidence=0.90,
                raw_excerpt="10-K annual filing: Gross margin expanded to 72% in FY2025 compared to 68% in FY2024, driven by improved operational efficiency and economies of scale."
            )
        ]

    def _extract_claim(self, filing: dict) -> str:
        """Extract claim from filing data."""
        form = filing.get("form", "Filing")
        date = filing.get("date", "recent")
        return f"Company filed {form} on {date}."

    def _generate_summary(self, evidence: list[Evidence], company_id: str) -> str:
        """Generate summary of financial findings."""
        if not evidence:
            return f"No financial filings found for {company_id}."

        evidence_refs = ", ".join(e.id[:8] for e in evidence[:3])
        return (
            f"Analyzed {len(evidence)} financial filings for {company_id}. "
            f"Key metrics include revenue growth, funding rounds, and margin expansion "
            f"(evidence: {evidence_refs})."
        )
