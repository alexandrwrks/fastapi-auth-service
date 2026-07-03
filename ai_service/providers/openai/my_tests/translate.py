import asyncio

from ai_service.models.models import TranslateRequest
from ai_service.providers.openai.main import open_ai_service


async def main():
    prompt = input("Введите запрос: ")
    language = input("Введите язык: ")

    print("Начало обработки запроса!\n")
    translated_text = await open_ai_service.translate(TranslateRequest(request=prompt, target_language=language))
    print(translated_text.response)


if __name__ == "__main__":
    asyncio.run(main())