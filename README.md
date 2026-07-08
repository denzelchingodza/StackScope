# StackScope
> Job search and scrapping application for devs.
---
Job market intelligence for developers. See what skills are in demand, what pays, and how your stack compares to what employers actually want.
---
## What it does

Scrapes live developer job postings from PNet, Careers24, and Indeed South Africa, then runs NLP and ML on the data to answer real questions:

- What skills are trending up or down?
- What salary range can I expect with my stack?
- How well do my skills match the current market, and what am I missing?

## Stack

Flask · SQLite · spaCy · scikit-learn · BeautifulSoup4 · Docker

## Running locally

```bash
git clone https://github.com/denzelchingodza/StackScope.git
cd StackScope
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python seed.py    # seed with starter data
python run.py     # scrape + start API
```

Open `frontend/index.html` in your browser.

---

Built by [Denzel Chingodza](https://denz-platform.vercel.app)
