from typing import Dict, Any, Optional
from ..core.models import Organization, AnalysisReport
from ..collectors.collector_manual import ManualCollector
from ..collectors.web_collector import WebCollector
from ..templates.registry import get_template

class AnalysisPipeline:
    def __init__(self, org: Organization, data_path: str = "", auto_collect: bool = False):
        self.org = org
        self.data_path = data_path
        self.auto_collect = auto_collect
        self.report = AnalysisReport(organization=org)
        self.report_path = ""

    def run(self) -> AnalysisReport:
        raw_data = {}
        if self.data_path:
            raw_data = ManualCollector(self.org, self.data_path).collect()
        elif self.auto_collect:
            raw_data = WebCollector(self.org.name, website=getattr(self.org, "website", "")).collect()
        if raw_data:
            self.report = get_template(self.org).build(raw_data)
        # generate charts if possible...
        self.report_path = "data/outputs/" + self.org.name.replace(" ", "_") + "_report.docx"
        return self.report