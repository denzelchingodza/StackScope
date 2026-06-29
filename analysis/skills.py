# analysis/skills.py

import logging
from collections import Counter
from itertools import combinations
from database.db import get_all_jobs

logger = logging.getLogger(__name__)


def get_skill_frequency(limit: int = 20) -> list[dict]:
    jobs = get_all_jobs()

    if not jobs:
        logger.warning("No jobs in database yet.")
        return []

    all_skills = []
    for job in jobs:
        if job["skills"]:
            skills = [s.strip() for s in job["skills"].split(",")]
            all_skills.extend(skills)

    counter = Counter(all_skills)
    total_jobs = len(jobs)

    results = []
    for skill, count in counter.most_common(limit):
        results.append({
            "skill": skill,
            "count": count,
            "percentage": round((count / total_jobs) * 100, 1)
        })

    return results


def get_skill_cooccurrence(min_count: int = 5) -> list[dict]:
    jobs = get_all_jobs()

    if not jobs:
        return []

    pair_counter = Counter()

    for job in jobs:
        if job["skills"]:
            skills = [s.strip() for s in job["skills"].split(",")]
            if len(skills) >= 2:
                for pair in combinations(sorted(skills), 2):
                    pair_counter[pair] += 1

    results = []
    for (skill_a, skill_b), count in pair_counter.most_common(30):
        if count >= min_count:
            results.append({
                "skill_a": skill_a,
                "skill_b": skill_b,
                "count": count
            })

    return results


def get_skills_by_experience(experience_level: str) -> list[dict]:
    jobs = get_all_jobs()

    if not jobs:
        return []

    filtered = [
        job for job in jobs
        if job["experience_level"] == experience_level
    ]

    if not filtered:
        logger.info(f"No jobs found for experience level: {experience_level}")
        return []

    all_skills = []
    for job in filtered:
        if job["skills"]:
            skills = [s.strip() for s in job["skills"].split(",")]
            all_skills.extend(skills)

    counter = Counter(all_skills)

    return [
        {"skill": skill, "count": count}
        for skill, count in counter.most_common(15)
    ]


def get_top_skills_by_source(source: str) -> list[dict]:
    jobs = get_all_jobs()

    if not jobs:
        return []

    filtered = [job for job in jobs if job["source"] == source]

    all_skills = []
    for job in filtered:
        if job["skills"]:
            skills = [s.strip() for s in job["skills"].split(",")]
            all_skills.extend(skills)

    counter = Counter(all_skills)

    return [
        {"skill": skill, "count": count}
        for skill, count in counter.most_common(10)
    ]