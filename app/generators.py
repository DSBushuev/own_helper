import os
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))

async def gpt(question):
    response = await client.chat.completions.create(
        messages=[{"role": "user",
                   "content": str(question)}],
        model="gpt-4o"
    )
    return response