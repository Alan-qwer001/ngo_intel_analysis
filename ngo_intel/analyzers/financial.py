from ..core.models import AnalysisReport, FinancialRecord, FinancialData
from .base import BaseAnalyzer
from typing import Dict, Any, List

class FinancialAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisReport:
        raw = getattr(self.report.organization, "financial_records", [])
        if not raw:
            return self.report
        records = []
        for r in raw:
            if isinstance(r, dict):
                records.append(FinancialRecord(**r))
            else:
                records.append(r)
        self.report.financial = FinancialData(
            records=records, currency="USD", unit="million",
            historical_total=getattr(self.report.organization, "historical_total", None),
            avg_annual_change=getattr(self.report.organization, "avg_annual_change", None),
        )
        self._calc_risk_matrix(records)
        self._calc_peer_comparison()
        self._calc_signals(records)
        return self.report

    def _calc_risk_matrix(self, records):
        if len(records) < 2: return
        sr = sorted(records, key=lambda r: r.year)
        latest, prev = sr[-1], sr[-2]
        all_regions = set(list(latest.regional_breakdown.keys()) + list(prev.regional_breakdown.keys()))
        changes = {}
        for reg in all_regions:
            new_v = latest.regional_breakdown.get(reg, 0)
            old_v = prev.regional_breakdown.get(reg, 0)
            if old_v > 0: changes[reg] = round((new_v - old_v) / old_v * 100, 1)
        rows = []
        for reg, chg in sorted(changes.items(), key=lambda x: x[1]):
            risk = "High" if chg < -40 else "Medium" if chg < -20 else "Low" if chg > 10 else "Stable"
            rows.append([reg, f"{chg:+.1f}%", risk, "From official financials"])
        self.report.risk_matrix_data = rows

    def _calc_peer_comparison(self):
        self.report.peer_comparison_data = [
            ["Dimension", "OSF", "Gates Foundation", "Ford Foundation", "Rockefeller"],
            ["2024 Expenditure", self._fmt(self._latest_total()), "~$7.5B", "~$600M", "~$200M"],
            ["Transparency", "Medium", "High (990)", "Mid-High", "Mid-High"],
            ["Risk Exposure", "Very High", "Very Low", "Low", "Low"],
        ]
    def _calc_signals(self, records):
        signals = []
        sr = sorted(records, key=lambda r: r.year)
        if len(sr) >= 3:
            y2, y3 = sr[-2], sr[-1]
            if y2.total_expenditure and y3.total_expenditure:
                chg = (y3.total_expenditure - y2.total_expenditure) / y2.total_expenditure * 100
                if chg < -30: signals.append(f"Expenditure dropped {chg:.0f}% -- restructuring")
                elif chg > 25: signals.append(f"Expenditure surged {chg:.0f}% -- transition")
        self.report.strategic_signals += signals

    def _latest_total(self):
        if self.report.financial and self.report.financial.records:
            return sorted(self.report.financial.records, key=lambda r: r.year)[-1].total_expenditure or 0
        return 0

    @staticmethod
    def _fmt(val):
        if val >= 1000: return f"${val/1000:.1f}B"
        return f"${val:.1f}M"

    def get_chart_data(self) -> Dict:
        if not self.report.financial: return {}
        records = sorted(self.report.financial.records, key=lambda r: r.year)
        years = [str(r.year) for r in records]
        totals = [r.total_expenditure or 0 for r in records]
        regions = set()
        for r in records: regions.update(r.regional_breakdown.keys())
        regions = sorted(regions)
        regional_by_year = []
        for r in records:
            row = {"year": str(r.year)}
            for reg in regions: row[reg] = r.regional_breakdown.get(reg, 0)
            regional_by_year.append(row)
        return {"years": years, "totals": totals, "regions": list(regions),
                "regional_data": regional_by_year, "latest_year": years[-1] if years else ""}