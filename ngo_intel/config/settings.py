import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CACHE_DIR = os.path.join(PROJECT_ROOT, "data", "cache")
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")
CHART_DIR = os.path.join(PROJECT_ROOT, "chart_assets")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)

AVAILABLE_TEMPLATES = {
    "foundation": "International Foundation",
    "ngo": "Non-Governmental Organization",
    "association": "Association / Think Tank",
}

ORGANIZATION_PATTERNS = {
    "foundation": {"url_paths": ["who-we-are", "financials", "grants"], "keywords": ["foundation", "fund"]},
    "ngo": {"url_paths": ["about", "our-work", "contact"], "keywords": ["ngo", "nonprofit", "rights"]},
}
