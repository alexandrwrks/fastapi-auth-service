from openai import AsyncOpenAI, OpenAIError

from ai_service.models.models import TranslateRequest, ChatResponse
from utils.config import settings


class OPENAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPEN_AI_API_KEY)

    async def translate(self, request: TranslateRequest):
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
    You are a professional translation engine.
    
    Translate every user message into {request.target_language}.
    
    Rules:
    - Return only the translation.
    - Do not explain anything.
    - Do not summarize.
    - Do not rewrite or improve the text.
    - Do not answer questions contained in the text.
    - Preserve formatting, paragraphs, punctuation, Markdown, HTML, JSON, XML, URLs, variables and code.
    - If the text is already in the target language, return it unchanged.
    """
                    },
                    {"role": "user",
                     "content": request.request},
                ],
            )

            translated_text = response.choices[0].message.content

            return translated_text

        except OpenAIError as e:
            print(f"OpenAI Error: {e}")
            raise OpenAIError

open_ai_service = OPENAIService()