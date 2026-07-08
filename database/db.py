# database/db.py
# Supports both PostgreSQL (production via DATABASE_URL) and SQLite (local dev fallback)

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "")
BACKEND = "postgres" if DATABASE_URL else "sqlite"

if BACKEND == "postgres":
    import psycopg2
    import psycopg2.extras
else:
    import sqlite3
    from config import DATABASE_PATH


def get_connection():
    if BACKEND == "postgres":
        return psycopg2.connect(DATABASE_URL)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_job(job: dict) -> bool:
    conn = get_connection()
    try:
        if BACKEND == "postgres":
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO jobs (
                    title, company, location, salary_raw,
                    salary_min, salary_max, description, skills,
                    experience_level, source, country, url,
                    date_posted, date_scraped
                ) VALUES (
                    %(title)s, %(company)s, %(location)s, %(salary_raw)s,
                    %(salary_min)s, %(salary_max)s, %(description)s, %(skills)s,
                    %(experience_level)s, %(source)s, %(country)s, %(url)s,
                    %(date_posted)s, %(date_scraped)s
                )
                ON CONFLICT (url) DO NOTHING
                RETURNING id
            """, {**job, "date_scraped": datetime.now().isoformat()})
            conn.commit()
            return cur.fetchone() is not None
        else:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO jobs (
                    title, company, location, salary_raw,
                    salary_min, salary_max, description, skills,
                    experience_level, source, country, url,
                    date_posted, date_scraped
                ) VALUES (
                    :title, :company, :location, :salary_raw,
                    :salary_min, :salary_max, :description, :skills,
                    :experience_level, :source, :country, :url,
                    :date_posted, :date_scraped
                )
            """, {**job, "date_scraped": datetime.now().isoformat()})
            conn.commit()
            return True
    except Exception as e:
        msg = str(e).lower()
        if "unique" in msg or "duplicate" in msg or "conflict" in msg:
            return False
        logger.error(f"save_job error: {e}")
        return False
    finally:
        conn.close()


def get_all_jobs(limit: int = 500) -> list:
    conn = get_connection()
    try:
        if BACKEND == "postgres":
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM jobs ORDER BY date_scraped DESC LIMIT %s", (limit,))
        else:
            cur = conn.cursor()
            cur.execute("SELECT * FROM jobs ORDER BY date_scraped DESC LIMIT ?", (limit,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def get_jobs_by_skill(skill: str) -> list:
    conn = get_connection()
    try:
        if BACKEND == "postgres":
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                "SELECT * FROM jobs WHERE skills ILIKE %s ORDER BY date_scraped DESC",
                (f"%{skill}%",)
            )
        else:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM jobs WHERE skills LIKE ? ORDER BY date_scraped DESC",
                (f"%{skill}%",)
            )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def get_job_count() -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM jobs")
        result = cur.fetchone()
        return result[0] if result else 0
    finally:
        conn.close()
