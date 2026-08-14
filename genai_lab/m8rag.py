import json
from pathlib import Path
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

def search_support_docs(query: str) -> dict:
    """Read-only search of the local support knowledge base."""
    results = collection.query(
        query_embeddings=[embed_one(query)],
        n_results=2,
        include=["documents", "metadatas"],
    )
    return {
        "sources": [
            {
                "id": source_id,
                "text": document,
                "metadata": metadata,
            }
            for source_id, document, metadata in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
            )
        ]
    }

search_tool = {
    "type": "function",
    "name": "search_support_docs",
    "description": (
        "Search the support knowledge base for policies and account-help information. "
        "Use this before answering a support-policy question."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The support question to search for.",
            }
        },
        "required": ["query"],
    },
}

user_question = """
A customer asks: How long does a refund take?

First, use search_support_docs.

For the final answer:
- State only facts explicitly present in the tool result.
- Cite the source ID in square brackets, for example [refunds].
- If the tool result does not support an answer, say:
  "I don't know based on the available support documents."
- Do not add general knowledge, assumptions, or extra advice.
""".strip()

first = client.interactions.create(
    model="gemini-3.6-flash",
    input=user_question,
    tools=[search_tool],
)

call = next(step for step in first.steps if step.type == "function_call")
print("Tool requested:", call.name, call.arguments)

result = search_support_docs(**call.arguments)
print("Tool result:", result)

final = client.interactions.create(
    model="gemini-3.6-flash",
    input=[
        {
            "type": "function_result",
            "name": call.name,
            "call_id": call.id,
            "result": [{"type": "text", "text": json.dumps(result)}],
        }
    ],
    tools=[search_tool],
    previous_interaction_id=first.id,
)

print("Final answer:", final.output_text)