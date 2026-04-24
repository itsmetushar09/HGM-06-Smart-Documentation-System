from config import qdrant_client as client
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
from functools import lru_cache
import os
import time
from services.embedding_model import get_embedder

# Load environment variables
load_dotenv()

# ======================
# API Keys
# ======================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

COLLECTION = "docs_vectors"


@lru_cache(maxsize=1)
def get_groq_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured")

    from groq import Groq

    return Groq(api_key=GROQ_API_KEY)


# ======================
# Safe Query Wrapper
# Prevents crashes if DNS fails once
# ======================

def safe_query(**kwargs):
    for _ in range(3):
        try:
            return client.query_points(**kwargs)
        except Exception as e:
            print("Retrying Qdrant query:", e)
            time.sleep(1)
    raise Exception("Qdrant temporarily unreachable")


# ======================
# RAG Answer Function
# ======================

def answer_question(question, repo, owner):
    embedder = get_embedder()

    # Convert question to embedding vector
    vector = embedder.encode(question).tolist()

    # Query repo-scoped embeddings
    hits = safe_query(
        collection_name=COLLECTION,
        query=vector,
        limit=5,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="repo",
                    match=MatchValue(value=repo)
                ),
                FieldCondition(
                    key="owner",
                    match=MatchValue(value=owner)
                )
            ]
        )
    )

    # Build context from retrieved chunks
    context = "\n\n".join(
        hit.payload.get("text", "")
        for hit in hits.points
    )

    if not context:
        return "No relevant documentation found for this repository."

    # Send context to Groq LLM
    completion = get_groq_client().chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You answer developer documentation questions."
            },
            {
                "role": "user",
                "content": f"{context}\n\nQuestion:\n{question}"
            }
        ]
    )

    return completion.choices[0].message.content
