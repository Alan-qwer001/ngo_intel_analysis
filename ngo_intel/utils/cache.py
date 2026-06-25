import json, os
from typing import Any, Dict, Optional
from ..config.settings import CACHE_DIR

def save(org_name: str, key: str, data: Any) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{org_name}_{key}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def load(org_name: str, key: str) -> Optional[Dict]:
    path = os.path.join(CACHE_DIR, f"{org_name}_{key}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def clear(org_name: str = None):
    for fn in os.listdir(CACHE_DIR):
        if org_name is None or fn.startswith(org_name):
            os.remove(os.path.join(CACHE_DIR, fn))
