# scraper/base.py

import re
import requests
import time
import logging
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from config import REQUEST_TIMEOUT, SCRAPE_DELAY, SKILLS

# Pre-compile one regex per skill using word boundaries.
# re.escape handles special chars like c#, c++, next.js, ci/cd.
_SKILL_PATTERNS = [
    (skill, re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE))
    for skill in SKILLS
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):

    def __init__(self, source: dict):
        self.source = source
        self.name = source["name"]
        self.url = source["url"]
        self.country = source["country"]
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def fetch(self, url: str) -> BeautifulSoup | None:
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            time.sleep(SCRAPE_DELAY)
            return BeautifulSoup(response.text, "html.parser")

        except requests.exceptions.Timeout:
            logger.warning(f"{self.name}: request timed out for {url}")
            return None

        except requests.exceptions.HTTPError as e:
            logger.warning(f"{self.name}: HTTP error {e} for {url}")
            return None

        except requests.exceptions.RequestException as e:
            logger.warning(f"{self.name}: request failed — {e}")
            return None

    def extract_skills(self, text: str) -> str:
        found = [skill for skill, pattern in _SKILL_PATTERNS if pattern.search(text)]
        return ", ".join(found)

    def detect_experience_level(self, text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ["senior", "lead", "principal", "staff"]):
            return "senior"
        if any(word in text_lower for word in ["mid", "intermediate", "3+ years", "4+ years"]):
            return "mid"
        if any(word in text_lower for word in ["junior", "graduate", "entry", "intern", "0-2", "1-2"]):
            return "junior"
        return "unspecified"

    def parse_salary(self, salary_str: str) -> tuple[float | None, float | None]:
        import re
        if not salary_str:
            return None, None

        numbers = re.findall(r"[\d\s,]+", salary_str.replace(" ", ""))
        cleaned = []
        for n in numbers:
            n = n.replace(",", "").strip()
            if n.isdigit():
                cleaned.append(float(n))

        if len(cleaned) >= 2:
            return min(cleaned), max(cleaned)
        if len(cleaned) == 1:
            return cleaned[0], None

        return None, None

    @abstractmethod
    def scrape(self) -> list[dict]:
        pass