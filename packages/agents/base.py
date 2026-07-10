"""Base agent class for Atlas."""

from abc import ABC, abstractmethod
import sys
import os

# Add schemas to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'schemas'))

from schemas.evidence import AgentReport


class BaseAgent(ABC):
    """Abstract base class for all Atlas agents."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent identifier."""
        pass

    @abstractmethod
    async def execute(self, company_id: str, run_id: str) -> AgentReport:
        """
        Execute research for a company and return evidence-backed report.

        Args:
            company_id: Company identifier
            run_id: Research run identifier for tracking

        Returns:
            AgentReport with evidence, summary, and signals
        """
        pass

    def validate_report(self, report: AgentReport) -> bool:
        """Validate that report meets evidence requirements."""
        # All evidence must have source_url (except demo_data)
        for evidence in report.evidence:
            if evidence.source_type != "demo_data" and not evidence.source_url:
                return False
            # All evidence must have non-empty claim and excerpt
            if not evidence.claim.strip() or not evidence.raw_excerpt.strip():
                return False
        return True
