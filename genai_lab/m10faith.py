import json

from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client()

schema = {
    "type": "object",
    "properties": {
        "supported": {"type": "boolean"},
        "unsupported_claims": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["supported", "unsupported_claims"],
}

source = "[refunds] Refunds are processed within five to seven business days."

answers = [
    "Refunds are processed within five to seven business days. [refunds]",
    (
        "Refunds are processed within five to seven business days. "
        "Your card issuer may take extra time to post the credit. [refunds]"
    ),
]

for answer in answers:
    prompt = f"""Decide whether every factual claim in the answer is supported by the source.
Use only the source. Do not use outside knowledge.
A source citation does not make an unsupported claim valid.

Source:
{source}

Answer:
{answer}
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

    verdict = json.loads(interaction.output_text)

    print(f"\nAnswer: {answer}")
    print("Faithful:", verdict["supported"])
    print("Unsupported claims:", verdict["unsupported_claims"])