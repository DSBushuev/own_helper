import os
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))

async def gpt(question):
    response = await client.chat.completions.create(
        extra_body={},
        model="z-ai/glm-4.5-air:free",
        messages=[{"role": "user",
                   "content": str(question)}]
        
    )
    return response