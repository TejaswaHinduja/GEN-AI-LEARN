import json
from google import genai

client = genai.Client()

question = "How long does a refund take?"

candidates = [
    "Refunds are processed within five to seven business days.",
    "Our office is open Monday to Friday, from 9am to 6pm.",
]

schema = {
    "type": "object",
    "properties": {
        "ranking": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source_id": {"type": "integer"},
                    "relevance": {"type": "integer"},
                },
                "required": ["source_id", "relevance"],
            },
        },
    },
    "required": ["ranking"],
}

prompt = f"""Rank the candidate passages for the question.
Use relevance from 0 (unrelated) to 10 (directly answers it).
Return every source exactly once.

Question: {question}

Sources:
[1] {candidates[0]}
[2] {candidates[1]}
"""

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": schema,
    },
)

ranking = json.loads(interaction.output_text)["ranking"]

for item in sorted(ranking, key=lambda item: item["relevance"], reverse=True):
    print(f"[{item['source_id']}] score={item['relevance']}: "
          f"{candidates[item['source_id'] - 1]}")