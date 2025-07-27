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

async def gpt(question):
    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="openchat/openchat-7b",
        messages=[{"role": "user", "content": str(question)}]
        extra_headers={
        "HTTP-Referer": "https://t.me/MyOwnHelper_chatBot",
        "X-Title": "my_helper"
    }
    )
    return response.choices[0].message.content
