from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY was not found in .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

response = client.chat.completions.create(
    model="qwen/qwen-2.5-7b-instruct",
    messages=[
        {
            "role": "user",
            "content": "Say hello and tell me that the API connection works."
        }
    ]
)

print(response.choices[0].message.content)