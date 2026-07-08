"""
start.py
--------
Production entry point.
- Creates tables and seeds mock data as fallback.
- Immediately starts the Flask API.
- Runs all scrapers in a background thread so real data loads without blocking startup.
"""

import sys
import os
import logging
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(__file__))

from database.models import create_tables
from database.db import get_job_count, save_job

create_tables()

# Seed mock data so the API has something to return immediately
if get_job_count() == 0:
    logger.info("Database empty — seeding with starter data")
    from seed import run as seed
    seed()
else:
    logger.info(f"Database has {get_job_count()} jobs")


def run_scrapers_background():
    """Run all scrapers in a background thread after startup."""
    logger.info("Background scrape starting...")
    try:
        from scraper.adzuna import AdzunaScraper
        from scraper.remotive import RemotiveScraper
        from scraper.weworkremotely import WeWorkRemotelyScraper
        from scraper.jobspresso import JobspressoScraper
        from config import SOURCES

        SCRAPER_MAP = {
            "adzuna": AdzunaScraper,
            "remotive": RemotiveScraper,
            "weworkremotely": WeWorkRemotelyScraper,
            "jobspresso": JobspressoScraper,
        }

        total_saved = 0
        total_skipped = 0

        for key, source in SOURCES.items():
            if not source.get("enabled"):
                continue
            scraper_class = SCRAPER_MAP.get(key)
            if not scraper_class:
                continue
            try:
                scraper = scraper_class(source)
                jobs = scraper.scrape()
                for job in jobs:
                    if save_job(job):
                        total_saved += 1
                    else:
                        total_skipped += 1
                logger.info(f"{source['name']}: {len(jobs)} jobs scraped")
            except Exception as e:
                logger.warning(f"{source['name']} scraper failed: {e}")

        logger.info(f"Background scrape done. Saved: {total_saved} | Duplicates skipped: {total_skipped}")
        logger.info(f"Total jobs in DB: {get_job_count()}")

    except Exception as e:
        logger.error(f"Background scrape crashed: {e}")


# Start scrapers in background — API is already up and serving while this runs
thread = threading.Thread(target=run_scrapers_background, daemon=True)
thread.start()

from config import API_PORT
from api.app import app

port = int(os.environ.get("PORT", API_PORT))
logger.info(f"Starting API on port {port}")
app.run(host="0.0.0.0", port=port, debug=False)
