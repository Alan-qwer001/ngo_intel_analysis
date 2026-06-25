from ..core.models import AnalysisReport, LegalRecord, LegalData
from .base import BaseAnalyzer
from typing import Dict, Any

class LegalRiskAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        records_raw = getattr(self.report.organization, "legal_records", [])
        if records_raw:
            records = [LegalRecord(**r) if isinstance(r, dict) else r for r in records_raw]
            self.report.legal = LegalData(records=records)
        
        compliance = getattr(self.report.organization, "compliance_mechanisms", [])
        if compliance and self.report.legal:
            self.report.legal.compliance_mechanisms = compliance
        return self.report
