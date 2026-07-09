# StackScope

Job market intelligence for developers. See which skills are in demand, what salaries look like, and how your stack compares to what employers actually want.

![Stack](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

---

## What it does

StackScope scrapes live developer job postings from Adzuna, Remotive, We Work Remotely, and Jobspresso. It runs NLP and machine learning on the data to answer real questions about the job market.

- Match your skills against live job demand and see where you stand
- Explore salary ranges by skill set and experience level
- Track which technologies are rising or declining week over week
- See which skills appear together most often in job postings

The core pipeline uses TF-IDF and cosine similarity built with spaCy and scikit-learn. Data lives in PostgreSQL on Supabase. A Flask API serves everything to a frontend built in plain HTML, CSS, and JavaScript.

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Web framework | Flask |
| NLP / ML | spaCy, scikit-learn |
| Database | PostgreSQL (Supabase) |
| Scraping | BeautifulSoup4, Requests |
| Container | Docker |
| Deployment | Render |

---

## Running locally

**1. Clone and set up the environment**

```bash
git clone https://github.com/denz-os/StackScope.git
cd StackScope
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**2. Create a `.env` file**

```env
DATABASE_URL=your_supabase_postgres_url
ADZUNA_APP_ID=your_adzuna_id
ADZUNA_APP_KEY=your_adzuna_key
```

Get a free Adzuna API key at [developer.adzuna.com](https://developer.adzuna.com).

**3. Seed and run**

```bash
python seed.py
python run.py
```

Open `frontend/index.html` in your browser.

---

## What I learned

Real data is messy. Salary fields came in every format across different currencies. A single-letter skill like "r" was matching inside every word in the English language until I fixed it with word-boundary regex. I migrated from SQLite to PostgreSQL halfway through because Render's ephemeral filesystem was resetting the database on every cold start.

Every one of those problems had a real solution. Finding them moved me further than any tutorial would have.

---


