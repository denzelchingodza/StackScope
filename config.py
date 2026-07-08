import os

# loads .env file if it exists (ignored by git)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

#DATABASE
DATABASE_PATH = os.environ.get("DATABASE_PATH", "database/stackscope.db")

#scraper sources
SOURCES = {
    # South Africa — via Adzuna API (free, no blocking)
    # Sign up: https://developer.adzuna.com
    # Set ADZUNA_APP_ID and ADZUNA_APP_KEY in your environment
    "adzuna": {
        "name": "Adzuna SA",
        "url": "https://api.adzuna.com/v1/api/jobs/za/search",
        "country": "ZA",
        "enabled": True,
    },
    # Remote worldwide
    "remotive": {
        "name": "Remotive",
        "url": "https://remotive.com/api/remote-jobs",
        "country": "REMOTE",
        "enabled": True,
    },
    "weworkremotely": {
        "name": "We Work Remotely",
        "url": "https://weworkremotely.com",
        "country": "REMOTE",
        "enabled": True,
    },
    "jobspresso": {
        "name": "Jobspresso",
        "url": "https://jobspresso.co",
        "country": "REMOTE",
        "enabled": True,
    },
}

#skills to track
SKILLS = [
    # Languages
    "python", "javascript", "typescript", "java", "c#", "c++", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "elixir", "clojure",
    # Frontend
    "react", "vue", "angular", "next.js", "node.js", "svelte", "tailwind",
    # Backend
    "django", "flask", "fastapi", "spring", "rails", "laravel", "express",
    "graphql", "rest", "grpc",
    # Data / ML / AI
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "spark", "airflow", "dbt", "llm", "openai", "langchain",
    # Databases
    "postgresql", "mysql", "mongodb", "sqlite", "redis", "elasticsearch",
    "dynamodb", "cassandra", "snowflake", "bigquery",
    # DevOps / Cloud / Infra
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible",
    "ci/cd", "github actions", "jenkins", "linux", "git",
    # Other
    "sql", "blockchain", "solidity", "cybersecurity", "embedded", "iot",
]

#scrap settings
REQUEST_TIMEOUT = 10
SCRAPE_DELAY = 2
MAX_PAGES = 5

#Flask API
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", 8080))
DEBUG = os.environ.get("DEBUG", "False") == "True"