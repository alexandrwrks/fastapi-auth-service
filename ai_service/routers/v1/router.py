from fastapi import APIRouter, Depends

from ai_service.models.models import TranslateRequest, ChatRequest
from ai_service.services.ai_service import ai_service
from deps import get_current_user

router = APIRouter(
    prefix="/ai/services",
    tags=["ai"],
)


@router.post("/chat")
async def chat(
        request_body: ChatRequest,
        current_user = Depends(get_current_user)
):
    return await ai_service.generate_text(request_body)


@router.post("/translate")
async def translate(
        request_body: TranslateRequest,
        current_user = Depends(get_current_user)
):
    return await ai_service.translate_text(request_body)



