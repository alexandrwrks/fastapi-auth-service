from fastapi import APIRouter

from ai_service.gemini.main import gemini_client
from deps import get_current_user

router = APIRouter(
    prefix="/ai/services",
    tags=["ai"],
)


@router.post("/")
async def ai_service(prompt: str):
    return await gemini_client.prompt(prompt)
