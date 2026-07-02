# StackScope

I built this because I was tired of guessing.

Every time I wanted to know what skills were actually in demand, or whether my stack was competitive, I had to manually scroll through dozens of job postings and piece things together in my head. There was no clean tool that gave developers in South Africa a real, data-driven picture of the market. So I built one. And now I use it.

StackScope scrapes live developer job postings from PNet, Careers24 and Indeed South Africa, processes the data using NLP and machine learning, and surfaces it in a clean interface that answers the questions developers actually care about. What skills are hiring managers looking for. What is rising and what is falling. What a realistic salary range looks like. And how your own stack compares to what the market wants right now.

---

## What it does

**Skill demand tracking** shows you the most requested skills across all current postings, updated every time you run a scrape. You can see not just the top skills but how frequently they co-occur, which tells you what employers expect you to know together.

**Trend analysis** detects which skills are growing in demand week over week and which are declining. It uses linear regression on time-series data to calculate the direction and rate of change, so you are looking at actual movement and not just raw counts.

**Salary intelligence** parses salary ranges out of unstructured job listing text, normalises the numbers, and gives you breakdowns by skill set and experience level. It can also predict a salary range based on the skills you provide.

**Skill matching** is the part I use most. You select the skills you have and the system compares your stack against the full job market using TF-IDF vectorisation and cosine similarity. It scores how well you match, tells you exactly what skills you have that employers want, and tells you what to learn next to close the gap.

**Jobs table** gives you a live, browsable view of the most recent postings with skills, experience level, and direct links back to the original listing on the source platform.

---

## Tech stack

The entire backend is Python. There is no framework overhead or unnecessary complexity, just the right tools for each job.

| Layer | Technology |
|---|---|
| Scraping | requests, BeautifulSoup4 |
| Database | SQLite with sqlite3 |
| NLP | spaCy (en_core_web_sm) |
| Matching | scikit-learn (TF-IDF, cosine similarity) |
| Salary prediction | scikit-learn (LinearRegression, MultiLabelBinarizer) |
| Trend analysis | numpy, statsmodels |
| API | Flask, flask-cors |
| Frontend | Plain HTML, CSS and JavaScript |
| Container | Docker, docker-compose |

---

## Running it locally

Requirements: Python 3.11, pip, Git

**1. Clone the repo**
```bash
git clone https://github.com/denzelchingodza/StackScope.git
cd StackScope
```

**2. Create a virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

**4. Seed the database with starter data**
```bash
python seed.py
```

**5. Start the API**
```bash
python -c "
import sys; sys.path.insert(0, '.')
from api.app import app
app.run(host='0.0.0.0', port=8080, debug=True)
"
```

**6. Open the frontend**

Open `frontend/index.html` in your browser. That is it.

---

## Running with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8080`.

---

## Project structure

```
StackScope/
  api/          Flask REST API and all endpoints
  analysis/     Skill frequency, salary, trends and job matching logic
  database/     SQLite models and all read and write operations
  scraper/      Base scraper class and individual scrapers per job board
  frontend/     HTML, CSS and JavaScript. No frameworks, no build step
  config.py     Central config for all settings
  run.py        Entry point: scrape then start API
  seed.py       Seeds the database with realistic data for local testing
```

---

## API reference

| Method | Endpoint | What it returns |
|---|---|---|
| GET | /api/health | Status and total job count |
| GET | /api/skills/frequency | Most demanded skills ranked by count |
| GET | /api/skills/cooccurrence | Skills that appear together in postings |
| GET | /api/salary/stats | Salary stats by skill and experience level |
| POST | /api/salary/predict | Predicted salary range for a given skill set |
| GET | /api/trends | Weekly skill trend data |
| GET | /api/trends/emerging | Skills growing in demand |
| GET | /api/trends/declining | Skills losing ground |
| POST | /api/match | Best matching jobs for a given skill set |
| POST | /api/gap | Market gap score and missing skills |
| GET | /api/jobs | All jobs in the database |

---

## Branches

`main` is stable, production ready code. `dev` is where active development happens. All new work goes to dev first and gets merged into main once it is tested and working.

---

## Disclaimer

StackScope is an independent personal project. It is not affiliated with Indeed, PNet or Careers24. All data is scraped from publicly available job listings for analytical and educational purposes only. Salary figures and skill statistics are estimates and should not be treated as financial or career advice.

---

Built by Denzel Chingodza
