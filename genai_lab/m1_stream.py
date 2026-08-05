
import os
from google import genai


from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

stream = client.models.generate_content_stream(
    model="gemini-3.6-flash",
    contents="Write a four-line poem about databases.",
)

for chunk in stream:
    print(chunk.text or "", end="", flush=True)

print()