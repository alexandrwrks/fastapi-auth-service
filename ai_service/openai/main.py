import os
from openai import OpenAI

from utils.config import settings

# Клиент автоматически загрузит ключ из переменной OPENAI_API_KEY
client = OpenAI(api_key=settings.OPEN_AI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Ты полезный ассистент."},
        {"role": "user", "content": "Напиши приветствие для нового пользователя."},
    ],
)

print(response.choices[0].message.content)
