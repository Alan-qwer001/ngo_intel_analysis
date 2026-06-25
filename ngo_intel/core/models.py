"""
NPO Intel Scout - Core data models.

Defines the structured data types used throughout the analysis pipeline.
All collectors produce these types, all analyzers consume them, and
report generators render them into documents.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime


@dataclass
class Organization:
    """Represents the target organization being analyzed."""
    name: str
    aliases: List[str] = field(default_factory=list)
    org_type: str = "ngo"
    registration_country: str = ""
    legal_form: str = ""
    founded_year: str = ""
    founder: str = ""
    headquarters: str = ""
    main_operating_entities: List[str] = field(default_factory=list)
    website: str = ""


@dataclass
class FinancialRecord:
    """Single year financial data point."""
    year: int
    total_expenditure: Optional[float] = None
    revenue: Optional[float] = None
    regional_breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class FinancialData:
    records: List[FinancialRecord] = field(default_factory=list)
    currency: str = "USD"
    unit: str = "million"
    historical_total: Optional[float] = None
    avg_annual_change: Optional[str] = None
    source_urls: List[str] = field(default_factory=list)


@dataclass
class Person:
    name: str
    title: str
    start_date: Optional[str] = None
    bio: Optional[str] = None


@dataclass
class GovernanceData:
    board_chair: Optional[Person] = None
    president: Optional[Person] = None
    executive_team: List[Person] = field(default_factory=list)
    board_members: List[Person] = field(default_factory=list)
    num_offices_global: Optional[int] = None
    num_employees: Optional[int] = None
    restructuring_notes: Optional[str] = None


@dataclass
class GrantRecord:
    year: int
    recipient: str
    amount: float
    term: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    funder_entity: Optional[str] = None


@dataclass
class GrantsData:
    records: List[GrantRecord] = field(default_factory=list)
    total_grants_found: Optional[int] = None


@dataclass
class LegalRecord:
    jurisdiction: str
    risk_level: str
    status: str
    trend: str
    description: str = ""
    details: List[str] = field(default_factory=list)


@dataclass
class LegalData:
    records: List[LegalRecord] = field(default_factory=list)
    compliance_mechanisms: List[str] = field(default_factory=list)


@dataclass
class TimelineEvent:
    date: str
    title: str
    impact: Optional[str] = None
    source_url: Optional[str] = None


@dataclass
class NewsData:
    events: List[TimelineEvent] = field(default_factory=list)
    total_items: Optional[int] = None


@dataclass
class PESTLEFactor:
    dimension: str
    factors: List[str] = field(default_factory=list)
    impact_level: str = "medium"


@dataclass
class PESTLEData:
    factors: List[PESTLEFactor] = field(default_factory=list)


@dataclass
class Initiative:
    date: str
    name: str
    scale: Optional[str] = None
    context: Optional[str] = None


@dataclass
class SevenSScore:
    strategy: int = 5
    structure: int = 5
    systems: int = 5
    shared_values: int = 5
    style: int = 5
    staff: int = 5
    skills: int = 5
    def total(self) -> int:
        return sum([self.strategy, self.structure, self.systems,
                    self.shared_values, self.style, self.staff, self.skills])


@dataclass
class AnalysisReport:
    """Final output of the analysis pipeline for one organization."""
    organization: Organization
    financial: Optional[FinancialData] = None
    governance: Optional[GovernanceData] = None
    grants: Optional[GrantsData] = None
    legal: Optional[LegalData] = None
    news: Optional[NewsData] = None
    pestle: Optional[PESTLEData] = None
    initiatives: List[Initiative] = field(default_factory=list)
    seven_s: Optional[SevenSScore] = None
    risk_matrix_data: List[List[str]] = field(default_factory=list)
    peer_comparison_data: List[List[str]] = field(default_factory=list)
    strategic_signals: List[str] = field(default_factory=list)
    conclusion_points: List[str] = field(default_factory=list)
    monitoring_suggestions: List[List[str]] = field(default_factory=list)
    intelligence_gaps: List[List[str]] = field(default_factory=list)
    critical_warnings: List[str] = field(default_factory=list)
    generated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")
