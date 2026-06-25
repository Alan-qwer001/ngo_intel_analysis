import requests, re, json
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class WebCollector:
    """通过访问组织官网，自动提取结构化数据。"""

    URL_PATTERNS = {
        "who_we_are": ["/who-we-are", "/about", "/about-us"],
        "financials": ["/who-we-are/financials", "/financials", "/financial-information"],
        "grants": ["/grants/past", "/our-grants", "/grants", "/awarded-grants"],
        "news": ["/newsroom", "/news", "/press", "/press-releases"],
        "leadership": ["/who-we-are/leadership", "/leadership", "/our-team", "/board"],
        "contact": ["/contact", "/contact-us", "/offices"],
    }

    def __init__(self, org_name: str, website: str = "", timeout: int = 15):
        self.org_name = org_name
        self.base_url = website or f"https://www.{org_name.lower().replace(' ','')}.org"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US"})
        self.extracted: Dict[str, Any] = {}
        self.confidence: Dict[str, str] = {}

    def collect(self) -> Dict[str, Any]:
        print(f"[采集] {self.org_name} -> {self.base_url}")
        if not self._reachable():
            print("[采集] 网站不可达"); return {}
        for category, paths in self.URL_PATTERNS.items():
            for path in paths:
                html = self._fetch(urljoin(self.base_url, path))
                if html:
                    getattr(self, f"_parse_{category}")(html)
                    break
        return self._output()

    def _reachable(self) -> bool:
        try: return self.session.head(self.base_url, timeout=5).status_code < 500
        except: return False

    def _fetch(self, url: str) -> Optional[str]:
        try:
            r = self.session.get(url, timeout=self.timeout)
            return r.text if r.status_code == 200 and len(r.text) > 500 else None
        except: return None

    def _parse_who_we_are(self, html: str):
        text = BeautifulSoup(html, "lxml").get_text(separator="\n", strip=True)
        m = re.search(r"(?:founded|established|since)\s*[:\s]*(\d{4})", text, re.I)
        if m: self.extracted["founded_year"] = m.group(1)

    def _parse_financials(self, html: str):
        soup = BeautifulSoup(html, "lxml")
        records = []
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = [c.get_text(strip=True) for c in row.find_all(["td","th"])]
                year = None; total = None
                for t in cells:
                    ym = re.search(r"\b(20\d{2})\b", t)
                    if ym: year = int(ym.group(1))
                    am = re.search(r"\$?([0-9,.]+)\s*(M|B|million|billion)", t, re.I)
                    if am:
                        v = float(am.group(1).replace(",",""))
                        if am.group(2).lower() in ("b","billion"): v *= 1000
                        total = v
                if year and total:
                    records.append({"year": year, "total_expenditure": total})
        if records:
            self.extracted["financial_records"] = records
            self.confidence["financials"] = "high"

    def _parse_grants(self, html: str):
        soup = BeautifulSoup(html, "lxml")
        grants = []
        for item in soup.find_all(["li","div","article"], class_=re.compile(r"grant|project", re.I))[:20]:
            t = item.get_text(strip=True)
            am = re.search(r"\$?([0-9,.]+)\s*(M|K|million|thousand)?", t)
            if am and len(t) > 20:
                v = float(am.group(1).replace(",",""))
                u = (am.group(2) or "").lower()
                if u in ("m","million"): v *= 1000000
                elif u in ("k","thousand"): v *= 1000
                if v > 10000: grants.append({"recipient": t[:40], "amount": v})
        if grants: self.extracted["grant_records"] = grants

    def _parse_news(self, html: str):
        events = []
        for link in BeautifulSoup(html, "lxml").find_all("a", href=True):
            t = link.get_text(strip=True)
            if len(t) > 25:
                dm = re.search(r"\b(20\d{2})\b", t)
                if dm: events.append({"date": dm.group(1), "title": t[:80]})
        if events: self.extracted["news_timeline"] = events[:10]

    def _parse_leadership(self, html: str):
        text = BeautifulSoup(html, "lxml").get_text(separator="\n", strip=True)
        m = re.search(r"(?:President|CEO|Chair|Chairman)\s*[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})", text)
        if m: self.extracted["registry_board_chair"] = {"name": m.group(1).strip()}

    def _parse_contact(self, html: str):
        text = BeautifulSoup(html, "lxml").get_text(separator="\n", strip=True)
        m = re.search(r"(?:Headquarters|Office)\s*[:\s]*([^。\n]{5,60})", text)
        if m and "headquarters" not in self.extracted:
            self.extracted["headquarters"] = m.group(1).strip()

    def _output(self) -> Dict[str, Any]:
        out = {k: self.extracted.get(k) for k in ["founded_year","headquarters","financial_records","grant_records","news_timeline","registry_board_chair"] if k in self.extracted}
        out["_notes"] = {"url": self.base_url, "confidence": self.confidence}
        return out