# StackScope

A job market intelligence tool for developers. Scrapes job boards, extracts skill demand data, and surfaces trends using NLP and machine learning.

## What it does

- Scrapes job postings from multiple sources daily
- Extracts and normalises skill mentions from unstructured job descriptions
- Tracks skill demand trends over time
- Predicts salary ranges by role and location
- Matches your skill set against the market and scores your gaps

## Tech Stack

- **Python** — as the core language
- **BeautifulSoup4 / requests** — for scraping
- **spaCy** — NLP and skill extraction
- **scikit-learn** — for job matching and salary prediction
- **statsmodels** — trend forecasting
- **SQLite** — local database
- **Flask** — REST API
- **HTML / CSS / JS** — frontend dashboard and design
- **Docker** — containerisation

## Project Structure
StackScope/

├── scraper/        # site specific scrapers

├── database/       # models and database logic

├── analysis/       # NLP, ML, and trend analysis

├── api/            # Flask REST API

├── frontend/       # HTML dashboard

├── config.py       # central configuration

├── run.py          # entry point

├── Dockerfile

└── docker-compose.yml


## Branches

- `main` — stable, working code
- `dev` — active development

## Setup

```bash
git clone https://github.com/denzelchingodza/StackScope.git
cd StackScope
pip install -r requirements.txt
python run.py
```

## Status

still in development phase!