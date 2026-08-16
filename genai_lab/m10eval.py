from pathlib import Path
from time import perf_counter
from dotenv import load_dotenv
import chromadb
from google import genai
load_dotenv()
client = genai.Client()

chroma_client = chromadb.PersistentClient(
    path=str(Path(__file__).parent / "chroma_db")
)
collection = chroma_client.get_collection("support_docs")

def embed_one(text: str) -> list[float]:
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return result.embeddings[0].values

def answer_question(question: str):
    results = collection.query(
        query_embeddings=[embed_one(question)],
        n_results=2,
        include=["documents"],
    )

    source_ids = results["ids"][0]
    documents = results["documents"][0]
    context = "\n".join(
        f"[{source_id}] {document}"
        for source_id, document in zip(source_ids, documents)
    )

    prompt = f"""Answer using only the source text below.
Use the source wording where possible.
Cite the source ID in square brackets.
If no source answers the question, say:
"I don't know based on the available support documents."

Sources:
{context}

Question: {question}
"""

    started = perf_counter()
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )
    latency_seconds = perf_counter() - started

    return interaction.output_text, source_ids, latency_seconds

golden_set = [
    {
        "question": "How long does a refund take?",
        "expected_source": "refunds",
    },
    {
        "question": "Where can I reset my password?",
        "expected_source": "password_reset",
    },
]

retrieval_passes = 0
citation_passes = 0

for case in golden_set:
    answer, source_ids, latency = answer_question(case["question"])

    retrieved_expected_source = case["expected_source"] in source_ids
    cites_expected_source = f"[{case['expected_source']}]" in answer

    retrieval_passes += retrieved_expected_source
    citation_passes += cites_expected_source

    print(f"\nQuestion: {case['question']}")
    print(f"Answer: {answer}")
    print(f"Retrieved: {source_ids}")
    print(
        f"retrieval={'PASS' if retrieved_expected_source else 'FAIL'} | "
        f"citation={'PASS' if cites_expected_source else 'FAIL'} | "
        f"latency={latency:.2f}s"
    )

total = len(golden_set)
print(f"\nRetrieval recall@2: {retrieval_passes / total:.0%}")
print(f"Citation coverage: {citation_passes / total:.0%}")