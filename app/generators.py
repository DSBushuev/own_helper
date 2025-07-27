import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("AI_TOKEN"),  # Ключ OpenRouter
    base_url="https://openrouter.ai/api/v1",  # Новый базовый адрес
    default_headers={
        "HTTP-Referer": "https://yourdomain.com",  # <-- желательно, но можно удалить
        "X-Title": "My Telegram Bot",              # <-- желательно, но можно удалить
    }
)

async def gpt(question):
    response = await client.chat.completions.create(
        model="openrouter/openchat",
        messages=[
            {"role": "user", "content": str(question)}
        ]
    )
    return response.choices[0].message.content
