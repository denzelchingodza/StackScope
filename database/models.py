import sqlite3
from config import DATABASE_PATH

def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT,
            location TEXT,
            salary_raw TEXT,
            salary_min REAL,
            salary_max REAL,
            description TEXT,
            skills TEXT,
            experience_level TEXT,
            source TEXT,
            country TEXT,
            url TEXT UNIQUE,
            date_posted TEXT,
            date_scraped TEXT
        )
    """)
    conn.commit()
    conn.close()

