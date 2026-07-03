from fastapi import HTTPException, status
from google.genai.errors import ServerError
from openai import OpenAIError

from ai_service.models.models import ChatRequest, ChatResponse, TranslateRequest
from ai_service.providers.gemini.main import gemini_service
from ai_service.providers.openai.main import open_ai_service


class AIService:
    async def generate_text(self, request: ChatRequest) -> ChatResponse:
        try:
            generated_text = await gemini_service.generate_text(request)

            return ChatResponse(response=generated_text)

        except ServerError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(e)
            )

    async def translate_text(self, request: TranslateRequest) -> ChatResponse:
        try:
            translated_text = await open_ai_service.translate(request)

            return ChatResponse(response=translated_text)

        except OpenAIError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(e)
            )

ai_service = AIService()