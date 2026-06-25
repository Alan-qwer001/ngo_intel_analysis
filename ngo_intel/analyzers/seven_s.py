from ..core.models import AnalysisReport, SevenSScore
from .base import BaseAnalyzer
from typing import Dict, Any

class SevenSAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        scores = getattr(self.report.organization, "seven_s_scores", None)
        if scores:
            self.report.seven_s = SevenSScore(**scores)
        
        # Auto-calc strategic_signals from seven_s scores
        if self.report.seven_s:
            s = self.report.seven_s
            signals = []
            if s.staff <= 5:
                signals.append("Staff dimension is the weakest link -- large-scale layoffs may have caused institutional memory loss")
            if s.strategy >= 8:
                signals.append("Strong strategic clarity -- direction is well-defined post-restructuring")
            if s.structure <= 6:
                signals.append("Structural integration still in progress -- near-term operational friction expected")
            self.report.strategic_signals = signals
        return self.report
