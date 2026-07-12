# StackScope

Job market intelligence for South African developers. Scrapes live job postings, extracts in-demand skills, tracks what's trending, and scores your stack against the current market.

![Stack](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

---

## What it does!

Scrapes developer job postings from Adzuna, Remotive, We Work Remotely, and Jobspresso and builds a structured picture of the market:

- What skills appear most frequently in job listings right now
- Which skills are trending up or down over time
- How your stack compares to what employers are asking for, scored using TF-IDF and cosine similarity
- Salary range estimates based on scraped posting data

The scoring system represents both job postings and a user's skill set as TF-IDF vectors, then computes cosine similarity to rank how well a profile matches the market. Skill extraction is done through keyword matching and frequency analysis across the scraped corpus.

---

## What it is

StackScope is a data pipeline and scoring tool. The core work is the scraping infrastructure, data cleaning, structured extraction, and ranking algorithm — not a machine learning model. It is accurately described as a job market intelligence tool with a keyword-based scoring engine.

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

Built by [Denzel Chingodza](https://denz-platform.vercel.app)
