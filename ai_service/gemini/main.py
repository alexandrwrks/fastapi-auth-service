from google import genai

from utils.config import settings


class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_AI_API_KEY

    async def prompt(self, prompt_text: str):
        client = genai.Client(api_key=self.api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",  # или gemini-2.5-pro для сложных задач
            contents=prompt_text,
        )

        return response.text

    async def admin_prompt(self, prompt_text: str):
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model="gemini-2.5-pro",  # или gemini-2.5-pro для сложных задач
            contents=prompt_text,
        )

        return response.text


gemini_client = GeminiClient()
