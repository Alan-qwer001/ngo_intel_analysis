import json
from typing import Dict, Any
from ..core.models import Organization
from .base import BaseCollector

class ManualCollector(BaseCollector):
    def __init__(self, org: Organization, json_path: str = ""):
        super().__init__(org)
        self.json_path = json_path
    
    def collect(self) -> Dict[str, Any]:
        if self.json_path:
            with open(self.json_path, "r", encoding="utf-8") as f:
                self.raw_data = json.load(f)
        return self.raw_data
    
    def collect_from_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.raw_data = data
        return self.raw_data
