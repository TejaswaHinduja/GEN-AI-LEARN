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

chroma_client = chromadb.PersistentClient(
    path=str(Path(__file__).parent / "chroma_db")
)
collection = chroma_client.get_collection("support_docs")

golden_set = [
    {
        "question": "When will I receive my refund?",
        "expected_id": "refunds",
    },
    {
        "question": "What time does the office open?",
        "expected_id": "office_hours",
    },
    {
        "question": "How can I change my password?",
        "expected_id": "password_reset",
    },
]

passed = 0

for test in golden_set:
    result = collection.query(
        query_embeddings=[embed_one(test["question"])],
        n_results=1,
    )
    actual_id = result["ids"][0][0]
    is_correct = actual_id == test["expected_id"]
    passed += is_correct

    print(
        f"{'PASS' if is_correct else 'FAIL'} | "
        f"{test['question']} → expected={test['expected_id']}, got={actual_id}"
    )

print(f"\nRecall@1: {passed / len(golden_set):.0%}")