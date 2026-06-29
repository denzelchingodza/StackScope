#DATABASE
DATABASE_PATH = "database/stackscope.db"

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
SCRAP_DELAY = 2
MAX_PAGES = 5

#Flask API
API_HOST = "0.0.0.0"
API_PORT = 5000
DEBUG = True