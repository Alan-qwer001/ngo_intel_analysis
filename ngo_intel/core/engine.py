import csv, os, json
from typing import List, Dict, Any
from ..core.models import Organization
from ..core.pipeline import AnalysisPipeline
from ..config.settings import DATA_DIR

class BatchEngine:
    """Batch processes a list of organizations."""
    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    def run_from_csv(self, csv_path: str):
        """Read organization names and optional data paths from CSV."""
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                org = Organization(name=row["name"], org_type=row.get("type", "ngo"))
                data_path = row.get("data_path", "")
                pipeline = AnalysisPipeline(org, data_path)
                report = pipeline.run()
                self.results.append({
                    "org": org.name,
                    "report_path": getattr(pipeline, "report_path", ""),
                    "warnings": report.critical_warnings,
                    "conclusion": report.conclusion_points,
                })
        return self.results

    def run_from_list(self, orgs: List[Organization]):
        for org in orgs:
            pipeline = AnalysisPipeline(org)
            report = pipeline.run()
            self.results.append({
                "org": org.name,
                "warnings": report.critical_warnings,
            })
        return self.results
