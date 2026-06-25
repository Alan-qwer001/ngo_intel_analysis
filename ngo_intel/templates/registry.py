from typing import Dict, Type
from ..core.models import Organization, AnalysisReport
from .base import BaseTemplate

_registry: Dict[str, Type[BaseTemplate]] = {}

def register(template_type: str, template_class: Type[BaseTemplate]):
    _registry[template_type] = template_class

def get_template(org: Organization) -> BaseTemplate:
    t = _registry.get(org.org_type)
    if t:
        return t(org)
    return _registry.get('ngo', lambda o: _registry['ngo'](org))(org)

def list_templates():
    return dict(_registry)
