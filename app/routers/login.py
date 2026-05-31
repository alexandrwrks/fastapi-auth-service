from fastapi import APIRouter, Request, status, Form
from fastapi.responses import HTMLResponse

from app.config_template import templates

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        status_code=status.HTTP_200_OK,
    )

@router.post("/")
async def login(
        email: str = Form(...),
        password: str = Form(...),
):
    print(email)
    print(password)

    return {"status": "ok"}