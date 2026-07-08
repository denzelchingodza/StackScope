# database/models.py

import os
import logging

logger = logging.getLogger(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "")


def create_tables():
    if DATABASE_URL:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id            SERIAL PRIMARY KEY,
                title         TEXT NOT NULL,
                company       TEXT,
                location      TEXT,
                salary_raw    TEXT,
                salary_min    FLOAT,
                salary_max    FLOAT,
                description   TEXT,
                skills        TEXT,
                experience_level TEXT,
                source        TEXT,
                country       TEXT,
                url           TEXT UNIQUE,
                date_posted   TEXT,
                date_scraped  TEXT
            )
        """)
        conn.commit()
        conn.close()
        logger.info("PostgreSQL tables ready.")
    else:
        import sqlite3
        from config import DATABASE_PATH
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                title         TEXT NOT NULL,
                company       TEXT,
                location      TEXT,
                salary_raw    TEXT,
                salary_min    REAL,
                salary_max    REAL,
                description   TEXT,
                skills        TEXT,
                experience_level TEXT,
                source        TEXT,
                country       TEXT,
                url           TEXT UNIQUE,
                date_posted   TEXT,
                date_scraped  TEXT
            )
        """)
        conn.commit()
        conn.close()
        logger.info("SQLite tables ready.")
