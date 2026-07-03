from google import genai
from google.genai.errors import ServerError

from ai_service.models.models import ChatRequest, ChatResponse
from utils.config import settings


from ai_service.providers.gemini.configs.configs import create_config


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_AI_API_KEY)

    async def generate_text(self, prompt: ChatRequest):
        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt.request,
                config=create_config()
            )

            return response.text

        except ServerError as e:
            print(f"Ошибка {e}")
            raise ServerError


gemini_service = GeminiService()
