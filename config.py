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
    "pnet": {
        "name": "PNet",
        "url": "https://www.pnet.co.za/jobs/it",
        "country": "ZA",
        "enabled": True,
    },
    "careers24": {
        "name": "Careers24",
        "url": "https://www.careers24.com/jobs/it",
        "country": "ZA",
        "enabled": True,
    },
    "indeed": {
        "name": "Indeed",
        "url": "https://za.indeed.com/jobs?q=software+developer",
        "country": "ZA",
        "enabled": True,
    }
}

#skills to track 
SKILLS = [
    "python", "javascript", "typescript", "java", "c#", "c++", "go", "rust",
    "react", "vue", "angular", "next.js", "node.js",
    "django", "flask", "fastapi", "spring",
    "postgresql", "mysql", "mongodb", "sqlite", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp",
    "git", "linux", "sql", "rest", "graphql",
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
]

#scrap settings
REQUEST_TIMEOUT = 10
SCRAPE_DELAY = 2
MAX_PAGES = 5

#Flask API
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", 8080))
DEBUG = os.environ.get("DEBUG", "False") == "True"