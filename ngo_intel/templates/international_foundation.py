from ..core.models import Organization, AnalysisReport, FinancialRecord, GrantRecord, LegalRecord, Initiative
from .base import BaseTemplate
from ..analyzers.financial import FinancialAnalyzer
from ..analyzers.overview import OverviewAnalyzer
from ..analyzers.legal_risk import LegalRiskAnalyzer
from ..analyzers.pestle import PESTLEAnalyzer
from ..analyzers.seven_s import SevenSAnalyzer
from ..analyzers.activities import ActivitiesAnalyzer
from ..analyzers.risk import RiskAnalyzer
from ..analyzers.synthesis import SynthesisAnalyzer
from typing import Dict, Any

class InternationalFoundationTemplate(BaseTemplate):
    def build(self, raw_data: Dict[str, Any]) -> AnalysisReport:
        org = Organization(name=self.org.name, org_type="foundation")
        report = AnalysisReport(organization=org)
        attr_map = [
            "financial_records", "legal_records", "grant_records",
            "pestle_factors", "seven_s_scores", "news_timeline",
            "initiatives", "compliance_mechanisms", "historical_total",
            "avg_annual_change", "registry_president", "registry_board_chair",
            "registry_offices", "registry_employees",
            "registration_country", "founded_year", "founder", "headquarters",
        ]
        for attr in attr_map:
            if attr in raw_data:
                setattr(report.organization, attr, raw_data[attr])
        for a in [
            OverviewAnalyzer(report), FinancialAnalyzer(report),
            ActivitiesAnalyzer(report), LegalRiskAnalyzer(report),
            PESTLEAnalyzer(report), SevenSAnalyzer(report),
            RiskAnalyzer(report), SynthesisAnalyzer(report),
        ]:
            report = a.analyze()
        return report