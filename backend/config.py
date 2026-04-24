import os
from pymongo import MongoClient
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# ======================
# MongoDB Configuration
# ======================

def _get_bool_env(name, default=False):
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

mongo_options = {}

if _get_bool_env("MONGO_TLS", MONGO_URI.startswith("mongodb+srv://")):
    mongo_options["tls"] = True
    mongo_options["tlsAllowInvalidCertificates"] = _get_bool_env(
        "MONGO_TLS_ALLOW_INVALID_CERTIFICATES",
        False
    )

mongo_client = MongoClient(
    MONGO_URI,
    **mongo_options
)

db = mongo_client["smartdocs"]

users_collection = db["users"]
docs_collection = db["docs"]
repos_collection = db["repos"]


# ======================
# Qdrant Configuration
# ======================

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_options = {
    "url": QDRANT_URL,
    "https": _get_bool_env("QDRANT_HTTPS", QDRANT_URL.startswith("https://")),
    "timeout": 30,
    "check_compatibility": False,
}

if QDRANT_API_KEY:
    qdrant_options["api_key"] = QDRANT_API_KEY

qdrant_client = QdrantClient(**qdrant_options)

print("Qdrant initialized:", bool(QDRANT_URL))
