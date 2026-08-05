import json
from google import genai
from dotenv import load_dotenv
load_dotenv()


client = genai.Client()

schema = {
    "type": "object",
    "properties": {
        "name": {"type": ["string", "null"]},
        "company": {"type": ["string", "null"]},
        "role": {"type": ["string", "null"]},
    },
    "required": ["name", "company", "role"],
    "additionalProperties": False,
}

text = "Hi, I'm Tejas, a GenAI learner building projects with Gemini,His mentor priya works at OpenAI."

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=f"Extract the person's name, company, and role only give out the person who has both company and a role ,from this text:\n{text}",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": schema,
    },
)

data = json.loads(interaction.output_text)
print(data)