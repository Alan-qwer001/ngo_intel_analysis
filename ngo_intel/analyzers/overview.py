from ..core.models import AnalysisReport, Organization, Person, GovernanceData, TimelineEvent, NewsData, Initiative
from .base import BaseAnalyzer
from typing import Dict, Any

class OverviewAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        data = self.report.organization
        r = self.report

        # Governance from raw_data
        gov_raw = r.organization
        gov = GovernanceData()
        gov.president = getattr(data, "registry_president", None)
        gov.board_chair = getattr(data, "registry_board_chair", None)
        gov.num_offices_global = getattr(data, "registry_offices", None)
        gov.num_employees = getattr(data, "registry_employees", None)
        r.governance = gov

        # Timeline from raw_data
        events_raw = getattr(data, "news_timeline", [])
        if events_raw:
            r.news = NewsData(events=[TimelineEvent(**e) for e in events_raw])

        # Initiatives
        init_raw = getattr(data, "initiatives", [])
        if init_raw:
            r.initiatives = [Initiative(**i) for i in init_raw]
        return r
