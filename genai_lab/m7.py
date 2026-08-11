from google import genai
from dotenv import load_dotenv
load_dotenv()
client = genai.Client()

document = """
# Refund Policy

## Refund timeline
Refunds are processed within five to seven business days after approval.
You will receive an email once the refund has been issued.

## Eligibility
Items must be returned unused and in their original packaging.

## Delays
Contact support if the refund does not appear after seven business days.
""".strip()

def split_by_heading(markdown):
    chunks = []
    heading = "Document"
    lines = []

    def save_chunk():
        text = "\n".join(lines).strip()
        if text:
            chunks.append({
                "section": heading,
                "text": f"{heading}\n{text}",
            })

    for line in markdown.splitlines():
        if line.startswith("#"):
            save_chunk()
            heading = line.lstrip("#").strip()
            lines = []
        else:
            lines.append(line)

    save_chunk()
    return chunks
for chunk in split_by_heading(document):
    token_count = client.models.count_tokens(
        model="gemini-3.6-flash",
        contents=chunk["text"],
    ).total_tokens

    print(f"\nSection: {chunk['section']} ({token_count} tokens)")
    print(chunk["text"])