from abc import ABC, abstractmethod
from typing import Any, Dict
from ..core.models import Organization, AnalysisReport

class BaseTemplate(ABC):
    def __init__(self, org: Organization):
        self.org = org
    @abstractmethod
    def build(self, raw_data: Dict[str, Any]) -> AnalysisReport:
        ...
