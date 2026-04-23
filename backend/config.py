import os
from pymongo import MongoClient
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# ======================
# MongoDB Configuration
# ======================

MONGO_URI = os.getenv("MONGO_URI")

mongo_client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = mongo_client["smartdocs"]

users_collection = db["users"]
docs_collection = db["docs"]
repos_collection = db["repos"]


# ======================
# Qdrant Configuration
# ======================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    https=True,
    timeout=30,
    check_compatibility=False
)

print("Qdrant initialized:", bool(QDRANT_URL))