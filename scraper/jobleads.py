# scraper/jobleads.py

import logging
from datetime import datetime
from bs4 import BeautifulSoup
from scraper.base import BaseScraper

logger = logging.getLogger(__name__)

# Search terms to pull developer jobs from JobLeads
SEARCH_TERMS = [
    "software+engineer",
    "python+developer",
    "data+engineer",
    "backend+developer",
    "machine+learning+engineer",
    "full+stack+developer",
]


class JobLeadsScraper(BaseScraper):
    SEARCH_URL = "https://www.jobleads.com/us/jobs/q/{query}"

    def scrape(self) -> list[dict]:
        jobs = []
        seen_urls: set[str] = set()
        logger.info(f"Starting scrape: {self.name}")

        for term in SEARCH_TERMS:
            url = self.SEARCH_URL.format(query=term)
            soup = self.fetch(url)
            if not soup:
                logger.warning(f"JobLeads: no response for term '{term}'")
                continue

            page_jobs = self._parse_page(soup)
            for job in page_jobs:
                if job["url"] not in seen_urls:
                    seen_urls.add(job["url"])
                    jobs.append(job)

            logger.info(f"JobLeads [{term}]: {len(page_jobs)} found")

        logger.info(f"{self.name} scrape complete. Total unique: {len(jobs)}")
        return jobs

    def _parse_page(self, soup: BeautifulSoup) -> list[dict]:
        jobs = []
        cards = soup.find_all("div", attrs={"data-testid": "search-job-card"})
        for card in cards:
            job = self._parse_card(card)
            if job:
                jobs.append(job)
        return jobs

    def _parse_card(self, card) -> dict | None:
        try:
            # Title
            h2 = card.find("h2")
            if not h2:
                return None
            title = h2.get_text(strip=True)
            if not title:
                return None

            # URL — invisible overlay anchor
            link = card.find("a", attrs={"data-testid": "search-job-card-link"})
            href = link["href"] if link else ""
            url = ("https://www.jobleads.com" + href) if href.startswith("/") else href

            # Company
            company_el = card.find("p", attrs={"data-testid": "search-job-card-company"})
            company = company_el.get_text(strip=True) if company_el else "Unknown"

            # Chips: location, work setting, salary
            location  = self._chip(card, "job-card-chip-location")
            salary_raw = self._chip(card, "job-card-chip-salary")

            salary_min, salary_max = self.parse_salary(salary_raw or "")
            skills = self.extract_skills(title)
            experience_level = self.detect_experience_level(title)

            return {
                "title": title,
                "company": company,
                "location": location or "Unknown",
                "salary_raw": salary_raw,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "description": "",
                "skills": skills,
                "experience_level": experience_level,
                "source": self.name,
                "country": "US",
                "url": url,
                "date_posted": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.warning(f"Failed to parse JobLeads card: {e}")
            return None

    def _chip(self, card, testid: str) -> str | None:
        """Extract text from a chip div by its data-testid."""
        el = card.find("div", attrs={"data-testid": testid})
        return el.get_text(strip=True) if el else None
