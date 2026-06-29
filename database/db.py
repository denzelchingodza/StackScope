#database/db.py
import sqlite3
from datetime import datetime
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def save_job(job: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
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
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
def get_all_jobs(limit: int = 500) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM jobs
        ORDER BY date_scraped DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
def get_jobs_by_skill(skill: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM jobs
        WHERE skills LIKE ?
        ORDER BY date_scraped DESC
    """, (f"%{skill}%",))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_job_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]
    conn.close()
    return count