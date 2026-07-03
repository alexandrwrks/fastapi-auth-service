import asyncio

from ai_service.models.models import TranslateRequest
from ai_service.providers.gemini.main import gemini_client



async def main():
    prompt = input("Введите запрос: ")
    language = input("Введите язык: ")

    print("Начало обработки запроса!\n")
    await gemini_client.generate_text(TranslateRequest(request=prompt, target_language=language))

if __name__ == "__main__":
    asyncio.run(main())