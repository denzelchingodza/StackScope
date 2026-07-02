# api/app.py

import logging
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from database.models import create_tables
from analysis.skills import (
    get_skill_frequency,
    get_skill_cooccurrence,
    get_skills_by_experience,
    get_top_skills_by_source,
)
from analysis.salary import get_salary_stats, predict_salary
from analysis.trends import get_trending_skills, get_emerging_skills, get_declining_skills, get_skill_trend
from analysis.matcher import match_jobs, get_gap_score
from database.db import get_all_jobs, get_job_count
from config import API_HOST, API_PORT, DEBUG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In production DEBUG is False (see config.py); never expose the interactive debugger
CORS(app, resources={r"/api/*": {"origins": os.environ.get("ALLOWED_ORIGINS", "*")}})

# Generic error handlers — no stack traces in responses
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error("Internal error: %s", e)
    return jsonify({"error": "Internal server error"}), 500

create_tables()


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "jobs_tracked": get_job_count()})


@app.route("/api/skills/frequency")
def skill_frequency():
    limit = request.args.get("limit", 20, type=int)
    return jsonify(get_skill_frequency(limit=limit))


@app.route("/api/skills/cooccurrence")
def skill_cooccurrence():
    return jsonify(get_skill_cooccurrence())


@app.route("/api/skills/experience/<level>")
def skills_by_experience(level):
    valid = ["junior", "mid", "senior"]
    if level not in valid:
        return jsonify({"error": f"Level must be one of {valid}"}), 400
    return jsonify(get_skills_by_experience(level))


@app.route("/api/skills/source/<source>")
def skills_by_source(source):
    return jsonify(get_top_skills_by_source(source))


@app.route("/api/salary/stats")
def salary_stats():
    return jsonify(get_salary_stats())


@app.route("/api/salary/predict", methods=["POST"])
def salary_predict():
    data = request.get_json()
    if not data or "skills" not in data or "experience_level" not in data:
        return jsonify({"error": "Provide skills and experience_level"}), 400

    result = predict_salary(data["skills"], data["experience_level"])
    if result is None:
        return jsonify({"error": "Not enough data to predict yet"}), 503

    return jsonify(result)


@app.route("/api/trends")
def trends():
    return jsonify(get_trending_skills())


@app.route("/api/trends/emerging")
def emerging():
    return jsonify(get_emerging_skills())


@app.route("/api/trends/declining")
def declining():
    return jsonify(get_declining_skills())


@app.route("/api/trends/<skill>")
def skill_trend(skill):
    return jsonify(get_skill_trend(skill))


@app.route("/api/match", methods=["POST"])
def match():
    data = request.get_json()
    if not data or "skills" not in data:
        return jsonify({"error": "Provide a skills list"}), 400

    skills = data["skills"]
    top_n = data.get("top_n", 10)
    return jsonify(match_jobs(user_skills=skills, top_n=top_n))


@app.route("/api/gap", methods=["POST"])
def gap():
    data = request.get_json()
    if not data or "skills" not in data:
        return jsonify({"error": "Provide a skills list"}), 400

    return jsonify(get_gap_score(user_skills=data["skills"]))


@app.route("/api/jobs")
def jobs():
    limit = request.args.get("limit", 100, type=int)
    return jsonify(get_all_jobs(limit=limit))


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG)