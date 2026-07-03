from pydantic import BaseModel


class ChatRequest(BaseModel):
    request: str


class TranslateRequest(BaseModel):
    request: str
    target_language: str

class ChatResponse(BaseModel):
    response: str | None
