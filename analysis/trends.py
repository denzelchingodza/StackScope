# analysis/trends.py

import logging
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta
from database.db import get_all_jobs
from config import SKILLS

logger = logging.getLogger(__name__)


def get_weekly_skill_counts() -> dict:
    jobs = get_all_jobs(limit=5000)

    if not jobs:
        return {}

    weekly = defaultdict(lambda: defaultdict(int))

    for job in jobs:
        if not job["skills"] or not job["date_scraped"]:
            continue

        try:
            date = datetime.fromisoformat(job["date_scraped"])
            week = date.strftime("%Y-W%W")
        except ValueError:
            continue

        skills = [s.strip() for s in job["skills"].split(",")]
        for skill in skills:
            weekly[week][skill] += 1

    return {week: dict(counts) for week, counts in sorted(weekly.items())}


def get_skill_trend(skill: str) -> dict:
    weekly = get_weekly_skill_counts()

    if not weekly:
        return {}

    weeks = sorted(weekly.keys())
    counts = [weekly[week].get(skill, 0) for week in weeks]

    if sum(counts) == 0:
        return {
            "skill": skill,
            "weeks": weeks,
            "counts": counts,
            "direction": "no data",
            "change_percent": 0,
        }

    direction, change_percent = _calculate_direction(counts)

    return {
        "skill": skill,
        "weeks": weeks,
        "counts": counts,
        "direction": direction,
        "change_percent": change_percent,
    }


def get_trending_skills(top_n: int = 10) -> list[dict]:
    weekly = get_weekly_skill_counts()

    if len(weekly) < 2:
        logger.warning("Need at least 2 weeks of data for trend analysis.")
        return []

    weeks = sorted(weekly.keys())
    results = []

    for skill in SKILLS:
        counts = [weekly[week].get(skill, 0) for week in weeks]

        if sum(counts) == 0:
            continue

        direction, change_percent = _calculate_direction(counts)

        results.append({
            "skill": skill,
            "direction": direction,
            "change_percent": change_percent,
            "recent_count": counts[-1],
            "weeks_tracked": len(weeks),
        })

    results.sort(key=lambda x: x["change_percent"], reverse=True)
    return results[:top_n]


def get_emerging_skills() -> list[dict]:
    trending = get_trending_skills(top_n=len(SKILLS))
    return [s for s in trending if s["direction"] == "rising" and s["change_percent"] > 20]


def get_declining_skills() -> list[dict]:
    trending = get_trending_skills(top_n=len(SKILLS))
    return [s for s in trending if s["direction"] == "declining" and s["change_percent"] < -20]


def _calculate_direction(counts: list[int]) -> tuple[str, float]:
    if len(counts) < 2:
        return "stable", 0.0

    x = np.array(range(len(counts)), dtype=float)
    y = np.array(counts, dtype=float)

    if np.std(y) == 0:
        return "stable", 0.0

    slope = np.polyfit(x, y, 1)[0]

    first_half = np.mean(y[:len(y)//2]) if len(y) >= 2 else y[0]
    second_half = np.mean(y[len(y)//2:]) if len(y) >= 2 else y[-1]

    if first_half == 0:
        change_percent = 100.0 if second_half > 0 else 0.0
    else:
        change_percent = round(((second_half - first_half) / first_half) * 100, 1)

    if slope > 0.5 and change_percent > 10:
        direction = "rising"
    elif slope < -0.5 and change_percent < -10:
        direction = "declining"
    else:
        direction = "stable"

    return direction, change_percent