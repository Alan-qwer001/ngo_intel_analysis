from ..core.models import AnalysisReport, PESTLEFactor, PESTLEData
from .base import BaseAnalyzer

class PESTLEAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        factors_raw = getattr(self.report.organization, "pestle_factors", [])
        if factors_raw:
            factors = [PESTLEFactor(**f) if isinstance(f, dict) else f for f in factors_raw]
            self.report.pestle = PESTLEData(factors=factors)
        return self.report
