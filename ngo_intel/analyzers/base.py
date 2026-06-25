from abc import ABC, abstractmethod
from typing import Any, Dict
from ..core.models import AnalysisReport

class BaseAnalyzer(ABC):
    def __init__(self, report: AnalysisReport):
        self.report = report
    @abstractmethod
    def analyze(self) -> AnalysisReport:
        ...
