document = """
Refunds are processed within five to seven business days after approval.
Items must be returned unused and in their original packaging.
You will receive an email once the refund has been issued.
Contact support if the refund does not appear after seven business days.
""".strip()

def chunk_words(text, size=12, overlap=3):
    words = text.split()
    step = size - overlap

    return [
        " ".join(words[start:start + size])
        for start in range(0, len(words), step)
    ]

chunks = chunk_words(document)

for index, chunk in enumerate(chunks, start=1):
    print(f"Chunk {index}: {chunk}")