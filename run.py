# run.py

import logging
from database.models import create_tables
from database.db import save_job
from scraper.pnet import PNetScraper
from scraper.indeed import IndeedScraper
from scraper.careers24 import Careers24Scraper
from scraper.remotive import RemotiveScraper
from scraper.weworkremotely import WeWorkRemotelyScraper
from scraper.jobspresso import JobspressoScraper
from config import SOURCES
from api.app import app, API_HOST, API_PORT, DEBUG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

SCRAPER_MAP = {
    "pnet": PNetScraper,
    "careers24": Careers24Scraper,
    "indeed": IndeedScraper,
    "remotive": RemotiveScraper,
    "weworkremotely": WeWorkRemotelyScraper,
    "jobspresso": JobspressoScraper,
}


def run_scrapers():
    logger.info("Starting scrape pipeline")
    create_tables()

    total_saved = 0
    total_skipped = 0

    for key, source in SOURCES.items():
        if not source.get("enabled"):
            logger.info(f"Skipping {source['name']} (disabled in config)")
            continue

        scraper_class = SCRAPER_MAP.get(key)
        if not scraper_class:
            logger.warning(f"No scraper found for key: {key}")
            continue

        scraper = scraper_class(source)
        jobs = scraper.scrape()

        for job in jobs:
            saved = save_job(job)
            if saved:
                total_saved += 1
            else:
                total_skipped += 1

    logger.info(f"Scrape complete. Saved: {total_saved} | Skipped (duplicates): {total_skipped}")


if __name__ == "__main__":
    run_scrapers()
    logger.info(f"Starting API on http://{API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)