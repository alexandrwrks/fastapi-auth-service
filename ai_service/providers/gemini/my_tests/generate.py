import asyncio

from ai_service.models.models import ChatRequest
from ai_service.providers.gemini.main import gemini_service



async def main():
    prompt = input("Введите запрос:")

    print("Начало обработки запроса!\n")
    await gemini_service.generate_text(ChatRequest(request=prompt))

if __name__ == "__main__":
    asyncio.run(main())