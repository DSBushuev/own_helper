import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),  # Ключ OpenRouter
    api_base="https://openrouter.ai/api/v1",  # Новый базовый адрес
)

async def gpt(question):
    response = await client.chat.completions.create(
        model="openchat/openchat-7b",
        messages=[
            {"role": "user", "content": str(question)}
        ]
    )
    return response.choices[0].message.content
