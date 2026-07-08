# scraper/jobspresso.py

import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from scraper.base import BaseScraper

logger = logging.getLogger(__name__)


class JobspressoScraper(BaseScraper):
    RSS_URL = "https://jobspresso.co/feed/"

    def scrape(self) -> list[dict]:
        jobs = []
        logger.info(f"Starting scrape: {self.name}")

        try:
            response = requests.get(self.RSS_URL, headers=self.headers, timeout=15)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            channel = root.find("channel")
            items = channel.findall("item") if channel is not None else []

            for item in items:
                job = self._parse_item(item)
                if job:
                    jobs.append(job)

            logger.info(f"Jobspresso: {len(items)} items found")

        except Exception as e:
            logger.warning(f"Jobspresso scrape failed: {e}")

        logger.info(f"{self.name} scrape complete. Total: {len(jobs)}")
        return jobs

    def _parse_item(self, item) -> dict | None:
        try:
            def text(tag):
                el = item.find(tag)
                return el.text.strip() if el is not None and el.text else ""

            title = text("title")
            if not title:
                return None

            url = text("link")
            description_html = text("description")
            description = BeautifulSoup(description_html, "html.parser").get_text()[:500]
            pub_date = text("pubDate") or datetime.now().isoformat()

            # Try to extract company from title (common format: "Job Title at Company")
            company = "Unknown"
            if " at " in title:
                parts = title.rsplit(" at ", 1)
                title = parts[0].strip()
                company = parts[1].strip()

            skills = self.extract_skills(title + " " + description)
            experience_level = self.detect_experience_level(title + " " + description)

            return {
                "title": title,
                "company": company,
                "location": "Remote",
                "salary_raw": None,
                "salary_min": None,
                "salary_max": None,
                "description": description,
                "skills": skills,
                "experience_level": experience_level,
                "source": self.name,
                "country": "REMOTE",
                "url": url,
                "date_posted": pub_date,
            }

        except Exception as e:
            logger.warning(f"Failed to parse Jobspresso item: {e}")
            return None
