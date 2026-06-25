from ..core.models import AnalysisReport, GrantRecord, GrantsData
from .base import BaseAnalyzer

class ActivitiesAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        raw = getattr(self.report.organization, 'grant_records', [])
        if raw:
            records = []
            for g in raw:
                if isinstance(g, dict):
                    records.append(GrantRecord(**g))
                else:
                    records.append(g)
            self.report.grants = GrantsData(records=records)
        return self.report
