# scraper/remotive.py

import logging
import requests
from datetime import datetime
from scraper.base import BaseScraper

logger = logging.getLogger(__name__)


class RemotiveScraper(BaseScraper):
    API_URL = "https://remotive.com/api/remote-jobs"

    def scrape(self) -> list[dict]:
        jobs = []
        logger.info(f"Starting scrape: {self.name}")

        try:
            response = requests.get(
                self.API_URL,
                params={"category": "software-dev", "limit": 100},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("jobs", []):
                job = self._parse_job(item)
                if job:
                    jobs.append(job)

        except Exception as e:
            logger.warning(f"Remotive scrape failed: {e}")

        logger.info(f"{self.name} scrape complete. Total: {len(jobs)}")
        return jobs

    def _parse_job(self, data: dict) -> dict | None:
        try:
            title = data.get("title", "").strip()
            if not title:
                return None

            company = data.get("company_name", "Unknown")
            location = data.get("candidate_required_location", "Remote") or "Remote"
            url = data.get("url", "")
            salary_raw = data.get("salary", "") or ""
            description = data.get("description", "") or ""

            # Strip HTML tags from description
            from bs4 import BeautifulSoup
            description_clean = BeautifulSoup(description, "html.parser").get_text()[:500]

            salary_min, salary_max = self.parse_salary(salary_raw)
            skills = self.extract_skills(title + " " + description_clean)
            experience_level = self.detect_experience_level(title + " " + description_clean)

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary_raw": salary_raw or None,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "description": description_clean,
                "skills": skills,
                "experience_level": experience_level,
                "source": self.name,
                "country": "REMOTE",
                "url": url,
                "date_posted": data.get("publication_date", datetime.now().isoformat()),
            }

        except Exception as e:
            logger.warning(f"Failed to parse Remotive job: {e}")
            return None
