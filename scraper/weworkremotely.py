# scraper/weworkremotely.py

import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from scraper.base import BaseScraper

logger = logging.getLogger(__name__)


class WeWorkRemotelyScraper(BaseScraper):
    RSS_URLS = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
        "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    ]

    def scrape(self) -> list[dict]:
        jobs = []
        logger.info(f"Starting scrape: {self.name}")

        for rss_url in self.RSS_URLS:
            try:
                response = requests.get(rss_url, headers=self.headers, timeout=15)
                response.raise_for_status()

                root = ET.fromstring(response.content)
                channel = root.find("channel")
                items = channel.findall("item") if channel is not None else []

                for item in items:
                    job = self._parse_item(item)
                    if job:
                        jobs.append(job)

                logger.info(f"WWR feed {rss_url}: {len(items)} items")

            except Exception as e:
                logger.warning(f"We Work Remotely feed failed ({rss_url}): {e}")

        logger.info(f"{self.name} scrape complete. Total: {len(jobs)}")
        return jobs

    def _parse_item(self, item) -> dict | None:
        try:
            def text(tag):
                el = item.find(tag)
                return el.text.strip() if el is not None and el.text else ""

            raw_title = text("title")
            if not raw_title:
                return None

            # WWR format: "Company: Job Title - Location"
            if ": " in raw_title:
                company, rest = raw_title.split(": ", 1)
                title = rest.split(" - ")[0].strip()
            else:
                company = "Unknown"
                title = raw_title

            url = text("link")
            description_html = text("description")
            description = BeautifulSoup(description_html, "html.parser").get_text()[:500]
            pub_date = text("pubDate") or datetime.now().isoformat()

            skills = self.extract_skills(title + " " + description)
            experience_level = self.detect_experience_level(title + " " + description)

            return {
                "title": title,
                "company": company.strip(),
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
            logger.warning(f"Failed to parse WWR item: {e}")
            return None
