"""
start.py
--------
Production entry point. Seeds the database then starts the Flask API.
Does not run scrapers (they require browser-like access not available in prod).
Use run.py locally if you want to scrape first.
"""

import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(__file__))

from database.models import create_tables
from database.db import get_job_count

create_tables()

if get_job_count() == 0:
    logger.info("Database is empty, seeding with starter data...")
    from seed import run as seed
    seed()
else:
    logger.info(f"Database has {get_job_count()} jobs, skipping seed")

from config import API_HOST, API_PORT
from api.app import app

port = int(os.environ.get("PORT", API_PORT))
logger.info(f"Starting API on port {port}")
app.run(host="0.0.0.0", port=port, debug=False)
