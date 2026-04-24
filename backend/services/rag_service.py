from config import qdrant_client as client
from qdrant_client.models import VectorParams, Distance
import uuid
import time
from services.embedding_model import get_embedder

# ======================
# Embedding Model
# ======================

COLLECTION = "docs_vectors"


# ======================
# Retry-safe helpers
# ======================

def safe_collection_exists(collection_name):

    for _ in range(3):
        try:
            return client.collection_exists(collection_name)
        except Exception as e:
            print("Retrying collection_exists:", e)
            time.sleep(1)

    raise Exception("Qdrant unavailable while checking collection")


def safe_create_collection(collection_name):

    for _ in range(3):
        try:
            return client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )
        except Exception as e:
            print("Retrying create_collection:", e)
            time.sleep(1)

    raise Exception("Failed to create collection")


def safe_upsert(collection_name, points):

    for _ in range(3):
        try:
            return client.upsert(
                collection_name=collection_name,
                points=points
            )
        except Exception as e:
            print("Retrying upsert:", e)
            time.sleep(1)

    raise Exception("Failed to upsert vectors")


# ======================
# Main embedding pipeline
# ======================

def embed_and_store(repo, owner, docs):
    if not docs:
        return

    model = get_embedder()

    # Ensure collection exists
    if not safe_collection_exists(COLLECTION):

        safe_create_collection(COLLECTION)

    # Extract text
    texts = [doc["content"] for doc in docs]

    # Generate embeddings
    vectors = model.encode(texts).tolist()

    # Prepare points
    points = []

    for doc, vector in zip(docs, vectors):

        points.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {
                "repo": repo,
                "owner": owner,
                "text": doc["content"]
            }
        })

    # Upload embeddings safely
    safe_upsert(COLLECTION, points)

    print(f"Embedded {len(points)} documents from repo: {repo}")
