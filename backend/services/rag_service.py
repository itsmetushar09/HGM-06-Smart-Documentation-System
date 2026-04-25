from config import qdrant_client as qdrant
from qdrant_client.models import VectorParams, Distance
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import uuid
import time
import os

load_dotenv()


hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))

COLLECTION = "docs_vectors"


def safe_collection_exists(collection_name):

    for _ in range(3):
        try:
            return qdrant.collection_exists(collection_name)
        except Exception as e:
            print("Retrying collection_exists:", e)
            time.sleep(1)

    raise Exception("Qdrant unavailable while checking collection")


def safe_create_collection(collection_name):

    for _ in range(3):
        try:
            return qdrant.create_collection(
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
            return qdrant.upsert(
                collection_name=collection_name,
                points=points
            )
        except Exception as e:
            print("Retrying upsert:", e)
            time.sleep(1)

    raise Exception("Failed to upsert vectors")




def embed_texts(texts):

    return hf_client.feature_extraction(
        texts,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )



def embed_and_store(repo, owner, docs):

    if not safe_collection_exists(COLLECTION):
        safe_create_collection(COLLECTION)

    texts = [doc["content"] for doc in docs]

    vectors = embed_texts(texts)

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

    safe_upsert(COLLECTION, points)

