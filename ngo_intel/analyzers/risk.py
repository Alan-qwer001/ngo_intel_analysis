from ..core.models import AnalysisReport
from .base import BaseAnalyzer

class RiskAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        warnings = []
        if self.report.legal:
            for r in self.report.legal.records:
                if r.risk_level == 'extreme':
                    warnings.append(r.jurisdiction + ': ' + r.status + ' - ' + r.description[:60])
                elif r.risk_level == 'high':
                    warnings.append(r.jurisdiction + ': ' + r.status)
        if self.report.seven_s and self.report.seven_s.staff <= 5:
            warnings.append('Large-scale layoffs created institutional memory gap')
        self.report.critical_warnings = warnings
        if self.report.financial and self.report.financial.records:
            records = sorted(self.report.financial.records, key=lambda r: r.year)
            if len(records) >= 2 and records[-1].total_expenditure and records[-2].total_expenditure:
                chg = (records[-1].total_expenditure - records[-2].total_expenditure) / records[-2].total_expenditure * 100
                if chg < -20:
                    warnings.append('Expenditure dropped by ' + f'{chg:.0f}' + '% year-on-year')
        return self.report
