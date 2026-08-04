import os
from google import genai
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

client = genai.Client()
print("Key loaded:", bool(os.environ.get("GEMINI_API_KEY")))


def quesAsk(ques:str)->str:
    chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a pirate. Answer in one sentence, pirate speak only.",
        temperature=0.7,
        ),
    )
    resp = chat.send_message(ques)
    return resp.text
    





print(quesAsk("can you explain the three stages of model buildng , pre traning , reinforcement learning, and i belive there was another stage before reeinforcement learning something on sueprvised learning"))
    