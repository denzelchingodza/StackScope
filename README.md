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

## What broke and how I fixed it

**Skill "r" matching inside every word**

The first version of skill extraction used `skill in text.lower()`. The skill `"r"` matched inside "developer", "engineer", "senior" every posting was flagged as requiring R. Fixed by pre-compiling one regex per skill using word boundaries:

```python
re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
```

`re.escape` also handles skills with special characters like `c#`, `c++`, and `next.js` that would otherwise break the regex pattern.

**Database wiped on every cold start**

The original build used SQLite with the database file stored on Render's local filesystem. Render's free tier uses ephemeral storage the filesystem resets on every deploy or cold start, taking all scraped data with it. Migrated to PostgreSQL on Supabase. Also added `ON CONFLICT (url) DO NOTHING` to the insert query so re-scraping the same job posting doesn't create duplicates.

**Salary fields in every format imaginable**

Scraped salary strings looked like `"$150k/year"`, `"£45,000 per annum"`, `"R25,000/month"`, `"$50/hr"`, and sometimes just `"competitive"`. Built a normaliser that detects k-notation, annual/monthly/hourly flags, and strips commas before extracting numbers. Any bare number above 5,000 is assumed annual and divided by 12. Hourly rates are multiplied by 160 (standard working hours per month).

**One failing scraper killing the whole pipeline**

If Remotive returned a 429 or We Work Remotely changed its HTML structure, an unhandled exception would crash the entire scrape run. Wrapped each scraper call in its own try/except block so a single failure is logged and skipped without stopping the rest of the queue.

**API blocked during scraping**

Running all four scrapers sequentially at startup blocked the Flask server for 15–30 seconds the API returned nothing until scraping finished. Fixed by moving scraping into a background thread:

```python
thread = threading.Thread(target=run_scrapers_background, daemon=True)
thread.start()
```

The API starts immediately and serves seed data while real data loads in the background. `daemon=True` ensures the thread dies automatically if the main process exits.

---

## Technical notes

- **Dual database backend** — `db.py` checks for a `DATABASE_URL` environment variable. If present it uses `psycopg2` (PostgreSQL). If not, it falls back to `sqlite3` for local development. Same query interface, different driver.
- **Skill extraction** — all skill patterns are pre compiled at import time into `_SKILL_PATTERNS`. Recompiling on every call would add significant overhead when processing hundreds of job descriptions.
- **TF-IDF scoring** — `TfidfVectorizer` is fit on the full corpus of job skill strings plus the user's skill string as the final document. The user vector is extracted as `tfidf_matrix[-1]` and compared against all job vectors using cosine similarity.
- **Salary currency detection** — checked by scanning for currency symbols and codes (`$`, `USD`, `£`, `GBP`, `R`, `ZAR`) before normalising to avoid mixing rand and dollar figures in the same stat.

---

Built by [Denzel Chingodza](https://denz-platform.vercel.app)
