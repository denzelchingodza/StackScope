# scraper/adzuna.py
#
# Uses the Adzuna Jobs API to fetch South African developer jobs.
# Free tier: 100 requests/day — enough for daily scrapes.
#
# Sign up at: https://developer.adzuna.com
# Add to Render env vars:
#   ADZUNA_APP_ID   = your app_id
#   ADZUNA_APP_KEY  = your app_key

import os
import logging
import requests
from datetime import datetime
from scraper.base import BaseScraper

logger = logging.getLogger(__name__)

APP_ID  = os.getenv("ADZUNA_APP_ID", "")
APP_KEY = os.getenv("ADZUNA_APP_KEY", "")

SEARCH_TERMS = [
    "software developer",
    "python developer",
    "javascript developer",
    "data engineer",
    "devops engineer",
    "full stack developer",
    "backend developer",
    "frontend developer",
]


class AdzunaScraper(BaseScraper):
    BASE_URL = "https://api.adzuna.com/v1/api/jobs/za/search"

    def scrape(self) -> list[dict]:
        if not APP_ID or not APP_KEY:
            logger.warning("Adzuna: ADZUNA_APP_ID or ADZUNA_APP_KEY not set, skipping.")
            return []

        jobs = []
        seen_urls = set()
        logger.info(f"Starting scrape: {self.name}")

        for term in SEARCH_TERMS:
            for page in range(1, 4):  # 3 pages per term = ~150 jobs per term
                try:
                    resp = requests.get(
                        f"{self.BASE_URL}/{page}",
                        params={
                            "app_id": APP_ID,
                            "app_key": APP_KEY,
                            "what": term,
                            "results_per_page": 50,
                            "content-type": "application/json",
                        },
                        timeout=15,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    results = data.get("results", [])

                    if not results:
                        break

                    for item in results:
                        job = self._parse_job(item)
                        if job and job["url"] not in seen_urls:
                            seen_urls.add(job["url"])
                            jobs.append(job)

                    logger.info(f"Adzuna '{term}' page {page}: {len(results)} results")

                except Exception as e:
                    logger.warning(f"Adzuna '{term}' page {page} failed: {e}")
                    break

        logger.info(f"{self.name} scrape complete. Total: {len(jobs)}")
        return jobs

    def _parse_job(self, data: dict) -> dict | None:
        try:
            title = (data.get("title") or "").strip()
            if not title:
                return None

            company = data.get("company", {}).get("display_name", "Unknown")
            location = data.get("location", {}).get("display_name", "South Africa")
            description = data.get("description", "") or ""
            url = data.get("redirect_url", "") or ""
            salary_min = data.get("salary_min")
            salary_max = data.get("salary_max")
            salary_raw = None
            if salary_min:
                salary_raw = f"R{int(salary_min):,} - R{int(salary_max):,}" if salary_max else f"R{int(salary_min):,}+"

            created = data.get("created", datetime.now().isoformat())

            skills = self.extract_skills(title + " " + description)
            experience_level = self.detect_experience_level(title + " " + description)

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary_raw": salary_raw,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "description": description[:500],
                "skills": skills,
                "experience_level": experience_level,
                "source": self.name,
                "country": "ZA",
                "url": url,
                "date_posted": created,
            }

        except Exception as e:
            logger.warning(f"Failed to parse Adzuna job: {e}")
            return None
