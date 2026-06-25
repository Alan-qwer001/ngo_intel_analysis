from abc import ABC, abstractmethod
from typing import Any, Dict
from ..core.models import Organization

class BaseCollector(ABC):
    def __init__(self, org: Organization):
        self.org = org
        self.raw_data: Dict[str, Any] = {}
    
    @abstractmethod
    def collect(self) -> Dict[str, Any]:
        ...
