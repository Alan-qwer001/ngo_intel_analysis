import os, json
from datetime import datetime
from ..core.models import AnalysisReport
from ..config.settings import OUTPUT_DIR
from .docx_generator import DocxGenerator

class ReportBuilder:
    def __init__(self, report: AnalysisReport):
        self.report = report

    def save(self, output_dir: str = "") -> str:
        od = output_dir or OUTPUT_DIR
        os.makedirs(od, exist_ok=True)
        safe_name = self.report.organization.name.replace(" ", "_")[:40]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        docx_path = os.path.join(od, f"{safe_name}_{timestamp}_report.docx")
        docx = DocxGenerator(self.report)
        docx.generate(docx_path)
        json_path = os.path.join(od, f"{safe_name}_{timestamp}_data.json")
        self._save_json(json_path)
        return docx_path

    def _save_json(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"organization_name": self.report.organization.name, "generated_at": self.report.generated_at, "conclusion_points": self.report.conclusion_points, "warnings": self.report.critical_warnings}, f, ensure_ascii=False, indent=2)
