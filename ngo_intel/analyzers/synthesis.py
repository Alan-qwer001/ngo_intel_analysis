from ..core.models import AnalysisReport
from .base import BaseAnalyzer

class SynthesisAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        points = []
        if self.report.financial:
            points.append('Financial data: ' + str(len(self.report.financial.records)) + ' years available')
        if self.report.legal:
            high_risk = [r for r in self.report.legal.records if r.risk_level in ('extreme', 'high')]
            points.append('Legal risk: ' + str(len(high_risk)) + ' elevated-risk jurisdictions')
        if self.report.seven_s:
            total = self.report.seven_s.total()
            label = 'Strong' if total > 45 else 'Moderate' if total > 35 else 'Weak'
            points.append('7S Score: ' + str(total) + '/70 - ' + label + ' organizational health')
        self.report.conclusion_points = points
        return self.report
