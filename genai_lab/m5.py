from pathlib import Path
import chromadb
from math import sqrt
from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client()

docs = [
    "Refunds are processed within five to seven business days.",
    "Our office is open Monday to Friday, from 9am to 6pm.",
    "Reset your password from the account settings page.",
]

def embed(texts):
    vectors = []

    for text in texts:
        result = client.models.embed_content(
            model="gemini-embedding-2",
            contents=text,
        )
        vectors.append(result.embeddings[0].values)

    return vectors

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    magnitude_a = sqrt(sum(x * x for x in a))
    magnitude_b = sqrt(sum(y * y for y in b))
    return dot / (magnitude_a * magnitude_b)

db_path = Path(__file__).parent / "chroma_db"
chroma_client = chromadb.PersistentClient(path=str(db_path))

collection = chroma_client.get_or_create_collection(
    name="support_docs",
    metadata={"hnsw:space": "cosine"},
)

doc_vectors = embed(docs)

collection.upsert(
    ids=["refunds", "office_hours", "password_reset"],
    metadatas=[
    {"topic": "billing"},
    {"topic": "operations"},
    {"topic": "account"},
],
    documents=docs,
    embeddings=doc_vectors,
)

query = "I sent an item back. When will the payment return to me?"
query_vector = embed([query])[0]

results = collection.query(
    query_embeddings=[query_vector],
    where={"topic": "billing"},
    n_results=1,
)

print("Best match:", results["documents"][0][0])
print("Cosine distance:", round(results["distances"][0][0], 3)) 