import re
from typing import List

def clean_html(html_text: str) -> str:
    import re
    clean = re.sub(r"<[^>]+>", "", html_text)
    return re.sub(r"\s+", " ", clean).strip()

def extract_money(text: str) -> List[float]:
    pattern = r"\$?([0-9]+(?:\.[0-9]+)?)\s*(M|B|K|\u4ebf|\u4e07)?"
    matches = re.findall(pattern, text)
    result = []
    for val, unit in matches:
        n = float(val)
        if unit in ("B", "\u4ebf"): n *= 1000
        elif unit == "K": n /= 1000
        elif unit == "\u4e07": n /= 100
        result.append(n)
    return result

def extract_years(text: str) -> List[int]:
    return [int(m) for m in re.findall(r"\b(20\d{2})\b", text)]

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")

def truncate(text: str, max_len: int = 80) -> str:
    return text[:max_len] + "..." if len(text) > max_len else text
