import json

from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

def add_numbers(first: int, second: int) -> dict:
    return {"total": first + second}

add_numbers_tool = {
    "type": "function",
    "name": "add_numbers",
    "description": "Adds two whole numbers.",
    "parameters": {
        "type": "object",
        "properties": {
            "first": {"type": "integer"},
            "second": {"type": "integer"},
        },
        "required": ["first", "second"],
    },
}

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Use the add_numbers tool to calculate 17 plus 25.",
    tools=[add_numbers_tool],
)

call = next(step for step in interaction.steps if step.type == "function_call")
print("Tool requested:", call.name, call.arguments)

result = add_numbers(**call.arguments)
print("Tool result:", result)

final_interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=[
        {
            "type": "function_result",
            "name": call.name,
            "call_id": call.id,
            "result": [{"type": "text", "text": json.dumps(result)}],
        }
    ],
    tools=[add_numbers_tool],
    previous_interaction_id=interaction.id,
)

print("Final answer:", final_interaction.output_text)