# scraper/indeed.py

import logging
from datetime import datetime
from scraper.base import BaseScraper
from config import MAX_PAGES

logger = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):

    def scrape(self) -> list[dict]:
        jobs = []
        logger.info(f"Starting scrape: {self.name}")

        for page in range(MAX_PAGES):
            start = page * 10
            url = f"{self.url}&start={start}"
            logger.info(f"Scraping page {page + 1}: {url}")

            soup = self.fetch(url)
            if soup is None:
                logger.warning(f"No response on page {page + 1}, stopping.")
                break

            listings = soup.find_all("div", class_="job_seen_beacon")

            if not listings:
                logger.info(f"No listings on page {page + 1}, stopping.")
                break

            for listing in listings:
                job = self._parse_listing(listing)
                if job:
                    jobs.append(job)

            logger.info(f"Page {page + 1}: found {len(listings)} listings")

        logger.info(f"{self.name} scrape complete. Total jobs: {len(jobs)}")
        return jobs

    def _parse_listing(self, listing) -> dict | None:
        try:
            title_tag = listing.find("span", attrs={"id": lambda x: x and x.startswith("jobTitle")})
            company_tag = listing.find("span", attrs={"data-testid": "company-name"})
            location_tag = listing.find("div", attrs={"data-testid": "text-location"})
            salary_tag = listing.find("div", class_="salary-snippet-container")
            url_tag = listing.find("a", class_="jcs-JobTitle")
            description_tag = listing.find("div", class_="job-snippet")

            title = title_tag.get_text(strip=True) if title_tag else None
            if not title:
                return None

            company = company_tag.get_text(strip=True) if company_tag else "Unknown"
            location = location_tag.get_text(strip=True) if location_tag else "Unknown"
            salary_raw = salary_tag.get_text(strip=True) if salary_tag else None
            description = description_tag.get_text(strip=True) if description_tag else ""
            job_path = url_tag["href"] if url_tag else None
            url = "https://za.indeed.com" + job_path if job_path else None

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