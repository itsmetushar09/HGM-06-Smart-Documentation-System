from config import qdrant_client as client
from qdrant_client.models import Filter, FieldCondition, MatchValue
<<<<<<< HEAD
from huggingface_hub import InferenceClient
=======
>>>>>>> parent of a89e188 (real fix)
from groq import Groq
from dotenv import load_dotenv
import os
import time

load_dotenv()



hf_client = InferenceClient(token=os.getenv("HF_TOKEN"))

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ======================
# Models
# ======================

groq_client = Groq(api_key=GROQ_API_KEY)

COLLECTION = "docs_vectors"


<<<<<<< HEAD
=======
# ======================
# Safe Query Wrapper
# Prevents crashes if DNS fails once
# ======================

>>>>>>> parent of a89e188 (real fix)
def safe_query(**kwargs):

    for _ in range(3):
        try:
            return client.query_points(**kwargs)
        except Exception as e:
            print("Retrying Qdrant query:", e)
            time.sleep(1)

    raise Exception("Qdrant temporarily unreachable")



<<<<<<< HEAD
def embed_query(question):
=======
def answer_question(question, repo):
    embedder = get_embedder()
>>>>>>> parent of a89e188 (real fix)

    return hf_client.feature_extraction(
        question,
        model="sentence-transformers/all-MiniLM-L6-v2"
    )



def answer_question(question, repo):

    vector = embed_query(question)

    hits = safe_query(
        collection_name=COLLECTION,
        query=vector,
        limit=5,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="repo",
                    match=MatchValue(value=repo)
                )
            ]
        )
    )

    context = "\n\n".join(
        hit.payload.get("text", "")
        for hit in hits.points
    )

    if not context:
        return "No relevant documentation found for this repository."

<<<<<<< HEAD
=======
    # Send context to Groq LLM
>>>>>>> parent of a89e188 (real fix)
    completion = groq_client.chat.completions.create(
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



