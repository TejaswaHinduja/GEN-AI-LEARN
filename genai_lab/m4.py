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

doc_vectors = embed(docs)
query = "How long will it take to receive my money back?"
query_vector = embed([query])[0]

scores = [cosine(query_vector, vector) for vector in doc_vectors]
print("Documents:", len(docs))
print("Vectors:", len(doc_vectors))
print("Scores:", len(scores))
best_index = max(range(len(docs)), key=lambda index: scores[index])

print("Best match:", docs[best_index])
print("Similarity:", round(scores[best_index], 3))