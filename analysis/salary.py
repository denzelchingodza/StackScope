# analysis/salary.py

import re
import logging
import numpy as np
from database.db import get_all_jobs

logger = logging.getLogger(__name__)

EXPERIENCE_MAP = {
    "junior": 0,
    "mid": 1,
    "senior": 2,
    "unspecified": 1,
}


def normalise_salary(salary_raw: str, period: str = "monthly") -> tuple[float | None, float | None]:
    if not salary_raw:
        return None, None

    text = salary_raw.lower().replace(",", "").replace(" ", "")
    is_annual = any(word in text for word in ["year", "annum", "annual", "pa", "yr"])
    is_hourly = "hour" in text or "/hr" in text

    numbers = re.findall(r"\d+(?:\.\d+)?k?", text)

    cleaned = []
    for n in numbers:
        if n.endswith("k"):
            cleaned.append(float(n[:-1]) * 1000)
        else:
            val = float(n)
            if val > 500:
                cleaned.append(val)

    if not cleaned:
        return None, None

    salary_min = min(cleaned)
    salary_max = max(cleaned) if len(cleaned) > 1 else None

    if is_annual:
        salary_min = salary_min / 12
        salary_max = salary_max / 12 if salary_max else None
    elif is_hourly:
        salary_min = salary_min * 160
        salary_max = salary_max * 160 if salary_max else None

    return round(salary_min, 2), round(salary_max, 2) if salary_max else None


def detect_currency(salary_raw: str) -> str:
    if not salary_raw:
        return "UNKNOWN"
    t = salary_raw.upper()
    if "USD" in t or "$" in t:
        return "USD"
    if "GBP" in t or "£" in t:
        return "GBP"
    if "EUR" in t or "€" in t:
        return "EUR"
    if "ZAR" in t or re.match(r"^R[\s\d]", salary_raw):
        return "ZAR"
    return "OTHER"


def get_salary_stats() -> dict:
    jobs = get_all_jobs()

    by_currency: dict[str, list[float]] = {}
    all_salaries = []

    for job in jobs:
        if not job["salary_min"]:
            continue
        currency = detect_currency(job.get("salary_raw") or "")
        by_currency.setdefault(currency, []).append(job["salary_min"])
        all_salaries.append(job["salary_min"])

    if not all_salaries:
        logger.warning("No salary data available yet.")
        return {}

    arr = np.array(all_salaries)

    symbols = {"USD": "$", "GBP": "£", "EUR": "€", "ZAR": "R", "OTHER": ""}
    currency_stats = {}
    for currency, vals in by_currency.items():
        if currency == "UNKNOWN":
            continue
        a = np.array(vals)
        currency_stats[currency] = {
            "symbol": symbols.get(currency, ""),
            "mean": round(float(np.mean(a)), 2),
            "median": round(float(np.median(a)), 2),
            "count": len(vals),
        }

    return {
        "count": len(all_salaries),
        "mean": round(float(np.mean(arr)), 2),
        "median": round(float(np.median(arr)), 2),
        "min": round(float(np.min(arr)), 2),
        "max": round(float(np.max(arr)), 2),
        "by_currency": currency_stats,
        "by_experience": get_salary_by_experience(),
    }


def get_salary_by_experience() -> dict:
    jobs = get_all_jobs()

    results = {}
    for level in ["junior", "mid", "senior"]:
        filtered = [
            job["salary_min"] for job in jobs
            if job["experience_level"] == level and job["salary_min"]
        ]
        if filtered:
            arr = np.array(filtered)
            results[level] = {
                "mean": round(float(np.mean(arr)), 2),
                "median": round(float(np.median(arr)), 2),
                "count": len(filtered),
            }

    return results


def predict_salary(skills: list[str], experience_level: str) -> dict | None:
    try:
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import MultiLabelBinarizer

        jobs = get_all_jobs()
        labelled = [
            job for job in jobs
            if job["salary_min"] and job["skills"] and job["experience_level"]
        ]

        if len(labelled) < 10:
            logger.warning("Not enough salary data to train a model yet.")
            return None

        mlb = MultiLabelBinarizer()
        skill_lists = [
            [s.strip() for s in job["skills"].split(",")]
            for job in labelled
        ]
        X_skills = mlb.fit_transform(skill_lists)

        X_experience = np.array([
            EXPERIENCE_MAP.get(job["experience_level"], 1)
            for job in labelled
        ]).reshape(-1, 1)

        X = np.hstack([X_skills, X_experience])
        y = np.array([job["salary_min"] for job in labelled])

        model = LinearRegression()
        model.fit(X, y)

        input_skills = mlb.transform([skills])
        input_experience = np.array([[EXPERIENCE_MAP.get(experience_level, 1)]])
        input_vector = np.hstack([input_skills, input_experience])

        prediction = model.predict(input_vector)[0]

        return {
            "predicted_min": round(max(prediction * 0.85, 0), 2),
            "predicted_max": round(prediction * 1.15, 2),
            "confidence": "low" if len(labelled) < 50 else "medium" if len(labelled) < 200 else "high",
            "based_on": len(labelled),
        }

    except Exception as e:
        logger.error(f"Salary prediction failed: {e}")
        return None