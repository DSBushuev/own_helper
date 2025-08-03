import asyncio
import os
from openai import OpenAI
from dotenv import load_dotenv
import urllib
from redis import asyncio as aioredis
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url='https://openrouter.ai/api/v1'
)

# Подключение к Redis (по умолчанию: localhost, порт 6379)
REDIS_URL="rediss://default:ARwrAAIjcDExYjkzMmYzOWYzMDA0ZGQ0ODY3ODQ5YWE5ZTg2MDVlM3AxMA@discrete-hedgehog-7211.upstash.io:6379"
if not REDIS_URL:
    raise ValueError("REDIS_URL не задан в переменных окружения")
parsed = urllib.parse.urlparse(REDIS_URL)


redis = aioredis.Redis(
    host=parsed.hostname,
    port=parsed.port,
    username=parsed.username,  # у upstash обычно это "default"
    password=parsed.password,
    ssl=True,
    decode_responses=True
)

MAX_MESSAGES = 6  # сколько сообщений хранить
MAX_TOTAL_CHARS = 3000  # сколько символов максимум отправлять GPT

async def save_message(user_id, role, content):
    key = f"chat:{user_id}"
    entry = json.dumps({"role": role, "content": content})
    await redis.rpush(key, entry)
    await redis.ltrim(key, -MAX_MESSAGES, -1)  # храним последние N сообщений

async def get_history(user_id):
    key = f"chat:{user_id}"
    entries = await redis.lrange(key, 0, -1)
    messages = []
    total_chars = 0

    for entry in reversed(entries):
        msg = json.loads(entry)
        msg_len = len(msg['content'])
        if total_chars + msg_len > MAX_TOTAL_CHARS:
            break
        total_chars += msg_len
        messages.insert(0, msg)

    return messages

async def gpt(user_id, question):
    try:
        # Получаем историю из Redis
        history = await get_history(user_id)

        # Добавляем текущий вопрос в конец истории
        messages = history + [{"role": "user", "content": question}]

        # Отправляем запрос к GPT с полной историей
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="openrouter/horizon-beta",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Сохраняем в Redis текущий вопрос и ответ
        await save_message(user_id, "user", question)
        await save_message(user_id, "assistant", reply)

        return reply

    except Exception as e:
        print(f"[GPT ERROR]: {e}")
        return "⚠️ Ошибка при обращении к ИИ. Попробуйте позже."