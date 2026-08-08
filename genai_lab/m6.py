from pathlib import Path

import chromadb
from google import genai
from dotenv import load_dotenv
load_dotenv()
model_client = genai.Client()

def embed_one(text):
    result = model_client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values

db_path = Path(__file__).parent / "chroma_db"
chroma_client = chromadb.PersistentClient(path=str(db_path))
collection = chroma_client.get_collection("support_docs")

question = "What is the customer-support phone number?"

results = collection.query(
    query_embeddings=[embed_one(question)],
    n_results=2,
    include=["documents", "metadatas"],
)

retrieved_docs = results["documents"][0]
context = "\n".join(
    f"[Source {index}] {document}"
    for index, document in enumerate(retrieved_docs, start=1)
)

prompt = f"""Answer the question using only the context below.
If the answer is not in the context, say: "I don't know based on the available documents."
Cite the source number you used.

Context:
{context}

Question: {question}
"""

interaction = model_client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
)

print("Answer:", interaction.output_text)
print("Retrieved sources:")
for index, document in enumerate(retrieved_docs, start=1):
    print(f"[{index}] {document}")