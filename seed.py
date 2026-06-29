"""
seed.py
-------
Seeds the database with realistic mock South African dev jobs.
Run this once to get data into the app so the API and frontend work.
Usage: python seed.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database.models import create_tables
from database.db import save_job

JOBS = [
    # PNet
    {"title": "Senior Python Developer",    "company": "DataVault Technologies", "location": "Cape Town",     "url": "https://www.pnet.co.za/jobs/job/1001", "source": "PNet",     "skills": "python,postgresql,docker,aws,rest",                    "salary_raw": "R85 000 per month",  "salary_min": 85000,  "salary_max": 110000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-15", "description": ""},
    {"title": "Junior JavaScript Developer", "company": "Clickatell",             "location": "Johannesburg", "url": "https://www.pnet.co.za/jobs/job/1002", "source": "PNet",     "skills": "javascript,react,node.js,git",                         "salary_raw": "R22 000 per month",  "salary_min": 22000,  "salary_max": 30000,  "experience_level": "junior", "country": "ZA", "date_posted": "2024-01-17", "description": ""},
    {"title": "Full Stack Engineer",         "company": "OfferZen",               "location": "Cape Town",    "url": "https://www.pnet.co.za/jobs/job/1003", "source": "PNet",     "skills": "react,node.js,postgresql,docker,typescript",           "salary_raw": "R60 000 per month",  "salary_min": 60000,  "salary_max": 80000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-18", "description": ""},
    {"title": "DevOps Engineer",             "company": "Standard Bank",          "location": "Johannesburg", "url": "https://www.pnet.co.za/jobs/job/1004", "source": "PNet",     "skills": "docker,kubernetes,aws,linux,python,git",               "salary_raw": "R75 000 per month",  "salary_min": 75000,  "salary_max": 95000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-19", "description": ""},
    {"title": "Machine Learning Engineer",   "company": "Aerobotics",             "location": "Cape Town",    "url": "https://www.pnet.co.za/jobs/job/1005", "source": "PNet",     "skills": "python,machine learning,tensorflow,pytorch,sql,scikit-learn", "salary_raw": "R90 000 per month", "salary_min": 90000, "salary_max": 120000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-20", "description": ""},
    {"title": "Backend Java Developer",      "company": "Absa Group",             "location": "Johannesburg", "url": "https://www.pnet.co.za/jobs/job/1006", "source": "PNet",     "skills": "java,spring,sql,postgresql,docker",                    "salary_raw": "R65 000 per month",  "salary_min": 65000,  "salary_max": 85000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-22", "description": ""},
    {"title": "Graduate Software Developer", "company": "Allan Gray",             "location": "Cape Town",    "url": "https://www.pnet.co.za/jobs/job/1007", "source": "PNet",     "skills": "python,java,sql,git",                                  "salary_raw": "R18 000 per month",  "salary_min": 18000,  "salary_max": 25000,  "experience_level": "junior", "country": "ZA", "date_posted": "2024-01-23", "description": ""},
    {"title": "Cloud Architect",             "company": "Dimension Data",         "location": "Johannesburg", "url": "https://www.pnet.co.za/jobs/job/1008", "source": "PNet",     "skills": "aws,azure,gcp,kubernetes,docker,linux",                "salary_raw": "R120 000 per month", "salary_min": 120000, "salary_max": 150000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-25", "description": ""},
    # Careers24
    {"title": "React Developer",             "company": "Superbalist",            "location": "Cape Town",    "url": "https://www.careers24.com/jobs/job/2001", "source": "Careers24", "skills": "react,javascript,typescript,node.js,git",              "salary_raw": "R45 000 per month",  "salary_min": 45000,  "salary_max": 65000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-16", "description": ""},
    {"title": "Senior Data Engineer",        "company": "Discovery Limited",      "location": "Sandton",      "url": "https://www.careers24.com/jobs/job/2002", "source": "Careers24", "skills": "python,sql,postgresql,aws,docker",                     "salary_raw": "R95 000 per month",  "salary_min": 95000,  "salary_max": 125000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-18", "description": ""},
    {"title": "Android Developer",           "company": "FNB Digital",            "location": "Johannesburg", "url": "https://www.careers24.com/jobs/job/2003", "source": "Careers24", "skills": "java,kotlin,rest,sql,git",                             "salary_raw": "R55 000 per month",  "salary_min": 55000,  "salary_max": 75000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-19", "description": ""},
    {"title": "Junior Data Analyst",         "company": "Takealot",               "location": "Cape Town",    "url": "https://www.careers24.com/jobs/job/2004", "source": "Careers24", "skills": "python,sql,postgresql,git",                            "salary_raw": "R20 000 per month",  "salary_min": 20000,  "salary_max": 28000,  "experience_level": "junior", "country": "ZA", "date_posted": "2024-01-20", "description": ""},
    {"title": "Platform Engineer",           "company": "Investec",               "location": "Johannesburg", "url": "https://www.careers24.com/jobs/job/2005", "source": "Careers24", "skills": "kubernetes,docker,aws,python,linux,go",                "salary_raw": "R100 000 per month", "salary_min": 100000, "salary_max": 130000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-21", "description": ""},
    {"title": "Vue.js Frontend Developer",   "company": "iKhokha",               "location": "Durban",       "url": "https://www.careers24.com/jobs/job/2006", "source": "Careers24", "skills": "vue,javascript,typescript,rest,git",                   "salary_raw": "R35 000 per month",  "salary_min": 35000,  "salary_max": 55000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-23", "description": ""},
    {"title": "Software Test Engineer",      "company": "Mukuru",                 "location": "Cape Town",    "url": "https://www.careers24.com/jobs/job/2007", "source": "Careers24", "skills": "python,javascript,sql,git,rest",                       "salary_raw": "R30 000 per month",  "salary_min": 30000,  "salary_max": 45000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-24", "description": ""},
    {"title": "Senior Full Stack Developer", "company": "Nando's Technology",     "location": "Johannesburg", "url": "https://www.careers24.com/jobs/job/2008", "source": "Careers24", "skills": "react,node.js,postgresql,docker,aws,typescript",       "salary_raw": "R80 000 per month",  "salary_min": 80000,  "salary_max": 105000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-26", "description": ""},
    # Indeed
    {"title": "Python Backend Developer",    "company": "Luno",                   "location": "Cape Town",    "url": "https://za.indeed.com/job/python-backend-3001", "source": "Indeed", "skills": "python,flask,postgresql,redis,docker,aws",            "salary_raw": "R75 000 per month",  "salary_min": 75000,  "salary_max": 95000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-15", "description": ""},
    {"title": "Junior React Developer",      "company": "Yoco Technologies",      "location": "Cape Town",    "url": "https://za.indeed.com/job/junior-react-3002",   "source": "Indeed", "skills": "react,javascript,typescript,git",                     "salary_raw": "R25 000 per month",  "salary_min": 25000,  "salary_max": 35000,  "experience_level": "junior", "country": "ZA", "date_posted": "2024-01-16", "description": ""},
    {"title": "Site Reliability Engineer",   "company": "Shoprite Group IT",      "location": "Brackenfell",  "url": "https://za.indeed.com/job/sre-3003",            "source": "Indeed", "skills": "linux,python,kubernetes,docker,aws,git",              "salary_raw": "R90 000 per month",  "salary_min": 90000,  "salary_max": 115000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-17", "description": ""},
    {"title": "TypeScript Developer",        "company": "Frogfoot Networks",      "location": "Paarl",        "url": "https://za.indeed.com/job/typescript-3004",     "source": "Indeed", "skills": "typescript,node.js,react,postgresql,git",             "salary_raw": "R50 000 per month",  "salary_min": 50000,  "salary_max": 70000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-18", "description": ""},
    {"title": "Data Science Lead",           "company": "Sanlam Group",           "location": "Bellville",    "url": "https://za.indeed.com/job/data-science-3005",   "source": "Indeed", "skills": "python,machine learning,scikit-learn,sql,aws,deep learning", "salary_raw": "R130 000 per month", "salary_min": 130000, "salary_max": 160000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-19", "description": ""},
    {"title": "Graduate Developer",          "company": "Woolworths Financial",   "location": "Cape Town",    "url": "https://za.indeed.com/job/graduate-dev-3006",   "source": "Indeed", "skills": "java,sql,git,python",                                 "salary_raw": "R20 000 per month",  "salary_min": 20000,  "salary_max": 20000,  "experience_level": "junior", "country": "ZA", "date_posted": "2024-01-20", "description": ""},
    {"title": "Go Backend Engineer",         "company": "Peach Payments",         "location": "Cape Town",    "url": "https://za.indeed.com/job/go-backend-3007",     "source": "Indeed", "skills": "go,postgresql,redis,docker,rest,aws",                 "salary_raw": "R85 000 per month",  "salary_min": 85000,  "salary_max": 110000, "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-21", "description": ""},
    {"title": "Senior Angular Developer",    "company": "Old Mutual",             "location": "Pinelands",    "url": "https://za.indeed.com/job/angular-3008",        "source": "Indeed", "skills": "angular,typescript,javascript,rest,git",              "salary_raw": "R70 000 per month",  "salary_min": 70000,  "salary_max": 90000,  "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-22", "description": ""},
    {"title": "Database Administrator",      "company": "Momentum Metropolitan",  "location": "Centurion",    "url": "https://za.indeed.com/job/dba-3009",            "source": "Indeed", "skills": "postgresql,mysql,sql,mongodb,linux",                  "salary_raw": "R60 000 per month",  "salary_min": 60000,  "salary_max": 80000,  "experience_level": "mid",    "country": "ZA", "date_posted": "2024-01-23", "description": ""},
    {"title": "Rust Systems Developer",      "company": "Synthesis Technology",   "location": "Remote",       "url": "https://za.indeed.com/job/rust-dev-3010",       "source": "Indeed", "skills": "rust,linux,docker,git,rest",                          "salary_raw": "R95 000 per month",  "salary_min": 95000,  "salary_max": 125000, "experience_level": "senior", "country": "ZA", "date_posted": "2024-01-24", "description": ""},
]


def run():
    create_tables()
    saved = 0
    skipped = 0
    for job in JOBS:
        ok = save_job(job)
        if ok:
            saved += 1
        else:
            skipped += 1

    print(f"Done. Saved: {saved} | Already existed: {skipped}")
    print(f"Total: {saved + skipped} jobs in database")


if __name__ == "__main__":
    run()
