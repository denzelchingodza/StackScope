# scraper/careers24.py

import logging
from datetime import datetime
from scraper.base import BaseScraper
from config import MAX_PAGES

logger = logging.getLogger(__name__)


class Careers24Scraper(BaseScraper):

    def scrape(self) -> list[dict]:
        jobs = []
        logger.info(f"Starting scrape: {self.name}")

        for page in range(1, MAX_PAGES + 1):
            url = f"{self.url}/p{page}"
            logger.info(f"Scraping page {page}: {url}")

            soup = self.fetch(url)
            if soup is None:
                logger.warning(f"No response on page {page}, stopping.")
                break

            listings = soup.find_all("article", class_="job-card")

            if not listings:
                logger.info(f"No listings on page {page}, stopping.")
                break

            for listing in listings:
                job = self._parse_listing(listing)
                if job:
                    jobs.append(job)

            logger.info(f"Page {page}: found {len(listings)} listings")

        logger.info(f"{self.name} scrape complete. Total jobs: {len(jobs)}")
        return jobs

    def _parse_listing(self, listing) -> dict | None:
        try:
            title_tag = listing.find("h2", class_="job-card__title")
            company_tag = listing.find("span", class_="job-card__company")
            location_tag = listing.find("span", class_="job-card__location")
            salary_tag = listing.find("span", class_="job-card__salary")
            url_tag = listing.find("a", class_="job-card__link", href=True)
            description_tag = listing.find("p", class_="job-card__description")

            title = title_tag.get_text(strip=True) if title_tag else None
            if not title:
                return None

            company = company_tag.get_text(strip=True) if company_tag else "Unknown"
            location = location_tag.get_text(strip=True) if location_tag else "Unknown"
            salary_raw = salary_tag.get_text(strip=True) if salary_tag else None
            description = description_tag.get_text(strip=True) if description_tag else ""
            job_path = url_tag["href"] if url_tag else None
            url = "https://www.careers24.com" + job_path if job_path and job_path.startswith("/") else job_path

            salary_min, salary_max = self.parse_salary(salary_raw)
            skills = self.extract_skills(title + " " + description)
            experience_level = self.detect_experience_level(title + " " + description)

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary_raw": salary_raw,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "description": description,
                "skills": skills,
                "experience_level": experience_level,
                "source": self.name,
                "country": self.country,
                "url": url,
                "date_posted": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.warning(f"Failed to parse listing: {e}")
            return None