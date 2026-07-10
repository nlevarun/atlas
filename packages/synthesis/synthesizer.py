"""Synthesis engine - converts evidence into narrative using FREE methods."""

from datetime import datetime, UTC
import sys
import os
from typing import Optional
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))

from schemas.evidence import AgentReport, Evidence
from schemas.company import CompanyProfile, NarrativeSection


class EvidenceSynthesizer:
    """
    Synthesizes agent evidence into coherent narratives with citations.

    Uses intelligent template-based synthesis - NO PAID APIs NEEDED.
    100% free, works offline, instant results.
    """

    def __init__(self, use_groq: bool = False):
        """
        Initialize synthesizer.

        Args:
            use_groq: Use Groq free tier LLM (optional, requires GROQ_API_KEY)
        """
        self.use_groq = use_groq

        # Groq is optional and free (15 requests/minute free tier)
        if use_groq:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                try:
                    from llm.groq_adapter import GroqProvider
                    self.llm = GroqProvider(api_key=api_key)
                except ImportError:
                    print("⚠️  Groq not available, using template synthesis")
                    self.llm = None
            else:
                self.llm = None
        else:
            self.llm = None

    async def synthesize(
        self,
        company_id: str,
        company_name: str,
        agent_reports: list[AgentReport]
    ) -> CompanyProfile:
        """
        Synthesize agent reports into company profile.

        Args:
            company_id: Company identifier
            company_name: Company name
            agent_reports: List of agent reports with evidence

        Returns:
            CompanyProfile with narrative sections
        """
        # Collect all evidence
        all_evidence = []
        for report in agent_reports:
            all_evidence.extend(report.evidence)

        # Generate each narrative section using template-based approach
        strategy = self._generate_strategy_section(company_name, all_evidence)
        growth = self._generate_growth_section(company_name, all_evidence)
        risks = self._generate_risks_section(company_name, all_evidence)

        return CompanyProfile(
            company_id=company_id,
            name=company_name,
            ticker=None,
            website=None,
            last_updated=datetime.now(UTC),
            current_strategy=strategy,
            growth_signals=growth,
            risks=risks,
            agent_reports=[report.dict() for report in agent_reports]
        )

    def _generate_strategy_section(
        self,
        company_name: str,
        evidence: list[Evidence]
    ) -> NarrativeSection:
        """Generate current strategy section using smart templates."""
        # Group evidence by type
        by_type = self._group_evidence_by_type(evidence)

        bullets = []
        evidence_ids = []

        # Strategy from news
        if "news" in by_type:
            news_evidence = by_type["news"][:2]  # Top 2 news items
            for e in news_evidence:
                bullet = self._extract_strategy_from_news(company_name, e)
                bullets.append(bullet)
                evidence_ids.append(e.id)

        # Strategy from financial data
        if "sec_filing" in by_type:
            financial = by_type["sec_filing"][0]
            bullet = self._extract_strategy_from_financials(company_name, financial)
            bullets.append(bullet)
            evidence_ids.append(financial.id)

        # Strategy from GitHub/tech presence
        if "github" in by_type:
            github = by_type["github"][0]
            bullet = self._extract_strategy_from_github(company_name, github)
            bullets.append(bullet)
            evidence_ids.append(github.id)

        # Fallback if no specific evidence
        if not bullets:
            bullets.append(f"{company_name} is operating in a competitive market with focus on innovation and growth.")
            evidence_ids = [e.id for e in evidence[:1]] if evidence else []

        return NarrativeSection(
            heading="Current Strategy",
            bullets=bullets,
            evidence_ids=evidence_ids
        )

    def _generate_growth_section(
        self,
        company_name: str,
        evidence: list[Evidence]
    ) -> NarrativeSection:
        """Generate growth signals section using smart templates."""
        by_type = self._group_evidence_by_type(evidence)

        bullets = []
        evidence_ids = []

        # Growth from hiring
        if "job_posting" in by_type:
            hiring = by_type["job_posting"]
            total_roles = len(hiring)
            if total_roles > 0:
                first = hiring[0]
                bullet = f"{company_name} is expanding its team with {total_roles} open positions, indicating active growth [{first.id[:8]}]."
                bullets.append(bullet)
                evidence_ids.extend([e.id for e in hiring[:3]])

        # Growth from financial metrics
        if "sec_filing" in by_type and len(by_type["sec_filing"]) > 1:
            financial = by_type["sec_filing"][1]
            if "growth" in financial.claim.lower() or "revenue" in financial.claim.lower():
                bullet = f"Financial metrics show positive momentum based on recent filings [{financial.id[:8]}]."
                bullets.append(bullet)
                evidence_ids.append(financial.id)

        # Growth from product launches (news)
        if "news" in by_type:
            for news in by_type["news"]:
                if any(word in news.claim.lower() for word in ["launch", "product", "release", "announce"]):
                    bullet = f"Recent product developments and market initiatives demonstrate forward momentum [{news.id[:8]}]."
                    bullets.append(bullet)
                    evidence_ids.append(news.id)
                    break

        # Growth from GitHub activity
        if "github" in by_type:
            github_items = by_type["github"]
            if github_items:
                total_stars = sum(1 for g in github_items if "star" in g.claim.lower())
                if total_stars > 0:
                    first = github_items[0]
                    bullet = f"Strong developer community engagement with active open-source presence [{first.id[:8]}]."
                    bullets.append(bullet)
                    evidence_ids.append(first.id)

        if not bullets:
            bullets.append(f"{company_name} shows signs of operational activity and market presence.")
            evidence_ids = [e.id for e in evidence[:2]] if evidence else []

        return NarrativeSection(
            heading="Growth Signals",
            bullets=bullets,
            evidence_ids=evidence_ids
        )

    def _generate_risks_section(
        self,
        company_name: str,
        evidence: list[Evidence]
    ) -> NarrativeSection:
        """Generate risks section by inferring from evidence."""
        by_type = self._group_evidence_by_type(evidence)

        bullets = []
        evidence_ids = []

        # Infer risks from growth signals
        if "job_posting" in by_type and len(by_type["job_posting"]) > 5:
            hiring = by_type["job_posting"][0]
            bullets.append(f"Rapid expansion may create scaling challenges and organizational complexity [{hiring.id[:8]}].")
            evidence_ids.append(hiring.id)

        # Market competition risk
        if "news" in by_type:
            news = by_type["news"][0]
            bullets.append(f"Operating in competitive market with evolving dynamics and emerging players [{news.id[:8]}].")
            evidence_ids.append(news.id)

        # Execution risk from multiple initiatives
        if len(evidence) > 10:
            bullets.append(f"Multiple concurrent initiatives require careful resource allocation and execution focus.")
            evidence_ids.extend([e.id for e in evidence[:2]])

        # Generic risks if nothing specific
        if not bullets:
            bullets.append(f"{company_name} faces standard industry risks including competition, market changes, and execution challenges.")
            evidence_ids = [e.id for e in evidence[:2]] if evidence else []

        # Always add standard risk disclaimer
        bullets.append("Market conditions and competitive landscape subject to rapid change requiring continuous adaptation.")

        return NarrativeSection(
            heading="Risks & Challenges",
            bullets=bullets,
            evidence_ids=evidence_ids[:3]  # Limit to 3 evidence refs
        )

    def _group_evidence_by_type(self, evidence: list[Evidence]) -> dict[str, list[Evidence]]:
        """Group evidence by source type."""
        grouped = {}
        for e in evidence:
            if e.source_type not in grouped:
                grouped[e.source_type] = []
            grouped[e.source_type].append(e)
        return grouped

    def _extract_strategy_from_news(self, company_name: str, evidence: Evidence) -> str:
        """Extract strategic insight from news evidence."""
        claim = evidence.claim.lower()

        if "partnership" in claim or "partner" in claim:
            return f"{company_name} is pursuing strategic partnerships to expand market reach and capabilities [{evidence.id[:8]}]."
        elif "launch" in claim or "product" in claim:
            return f"{company_name} is actively developing and launching new products to capture market opportunities [{evidence.id[:8]}]."
        elif "funding" in claim or "raised" in claim:
            return f"{company_name} is securing capital to fuel growth and strategic initiatives [{evidence.id[:8]}]."
        elif "expansion" in claim or "expand" in claim:
            return f"{company_name} is expanding into new markets and customer segments [{evidence.id[:8]}]."
        else:
            return f"{company_name} is executing on strategic initiatives including {evidence.claim[:50]}... [{evidence.id[:8]}]."

    def _extract_strategy_from_financials(self, company_name: str, evidence: Evidence) -> str:
        """Extract strategic insight from financial evidence."""
        claim = evidence.claim.lower()

        if "revenue" in claim or "growth" in claim:
            return f"{company_name} demonstrates financial discipline with focus on sustainable revenue growth [{evidence.id[:8]}]."
        elif "margin" in claim:
            return f"{company_name} is optimizing operational efficiency and margin structure [{evidence.id[:8]}]."
        elif "funding" in claim or "raised" in claim:
            return f"{company_name} has secured financial resources to execute long-term strategy [{evidence.id[:8]}]."
        else:
            return f"{company_name} maintains focus on financial performance and operational metrics [{evidence.id[:8]}]."

    def _extract_strategy_from_github(self, company_name: str, evidence: Evidence) -> str:
        """Extract strategic insight from GitHub evidence."""
        claim = evidence.claim.lower()

        if "stars" in claim or "forks" in claim:
            return f"{company_name} is building developer community and open-source ecosystem [{evidence.id[:8]}]."
        else:
            return f"{company_name} maintains active technical development and community engagement [{evidence.id[:8]}]."
