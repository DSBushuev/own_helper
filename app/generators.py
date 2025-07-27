import os
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print("OpenRouter API Key:", repr(os.getenv("OPENROUTER_API_KEY")))

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def gpt(question):
    response = client.chat.completions.create(
        extra_headers={
        "HTTP-Referer": "https://t.me/MyOwnHelper_chatBot",
        "X-Title": "my_helper"},
        model="openchat/openchat-7b",
        messages=[{"role": "user", "content": str(question)}]
        )
    return response.choices[0].message.content
