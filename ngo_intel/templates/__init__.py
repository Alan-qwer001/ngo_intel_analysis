from .international_foundation import InternationalFoundationTemplate
from .registry import register
register("foundation", InternationalFoundationTemplate)
register("ngo", InternationalFoundationTemplate)