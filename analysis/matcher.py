# analysis/matcher.py

import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.db import get_all_jobs
from config import SKILLS

logger = logging.getLogger(__name__)


def match_jobs(user_skills: list[str], top_n: int = 10) -> list[dict]:
    jobs = get_all_jobs()

    if not jobs:
        logger.warning("No jobs in database yet.")
        return []

    jobs_with_skills = [job for job in jobs if job["skills"]]

    if not jobs_with_skills:
        return []

    job_skill_strings = [job["skills"] for job in jobs_with_skills]
    user_skill_string = ", ".join(user_skills)

    all_documents = job_skill_strings + [user_skill_string]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_documents)

    user_vector = tfidf_matrix[-1]
    job_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(user_vector, job_vectors)[0]

    top_indices = np.argsort(similarities)[::-1][:top_n]

    results = []
    for idx in top_indices:
        job = jobs_with_skills[idx]
        score = round(float(similarities[idx]) * 100, 1)

        job_skills = [s.strip() for s in job["skills"].split(",")]
        matched = [s for s in user_skills if s.lower() in job_skills]
        missing = [s for s in job_skills if s not in [u.lower() for u in user_skills]]

        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "source": job["source"],
            "url": job["url"],
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing[:5],
            "experience_level": job["experience_level"],
            "salary_min": job["salary_min"],
            "salary_max": job["salary_max"],
        })

    return results


def get_gap_score(user_skills: list[str]) -> dict:
    jobs = get_all_jobs()

    if not jobs:
        return {}

    all_skills = []
    for job in jobs:
        if job["skills"]:
            skills = [s.strip() for s in job["skills"].split(",")]
            all_skills.extend(skills)

    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = [skill for skill, _ in skill_counts.most_common(20)]

    user_lower = [s.lower() for s in user_skills]

    have = [s for s in top_skills if s in user_lower]
    missing = [s for s in top_skills if s not in user_lower]

    score = round((len(have) / len(top_skills)) * 100, 1)

    return {
        "score": score,
        "have": have,
        "missing": missing,
        "total_tracked": len(top_skills),
        "summary": _score_summary(score),
    }


def _score_summary(score: float) -> str:
    if score >= 80:
        return "Strong market alignment. You match most in-demand skills."
    if score >= 60:
        return "Good alignment. A few key skills could improve your position significantly."
    if score >= 40:
        return "Moderate alignment. Focus on the missing skills to become more competitive."
    return "Early stage. The missing skills list is your learning roadmap."