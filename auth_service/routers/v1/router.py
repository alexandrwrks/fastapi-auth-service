from fastapi import APIRouter, Depends, BackgroundTasks

from auth_service.schemas import LoginSchema, RefreshSchema, RegisterSchema
from auth_service.services.auth import AuthService
from deps import get_auth_service, get_current_user
from notification_service.email_service.email_service import email_service

router = APIRouter(prefix="/auth_service", tags=["auth_service"])

"""
router  v1/auth_srvice

после регистрации приходит сообщение об успешной регистрации на почту
с помощью notification_service


получение JWT access/refresh token-ы после успешной авторизации


/refresh - для обновления токенов
/logout - отменяет refresh token в БД
"""


@router.post("/register")
async def register(
    data: RegisterSchema,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(get_auth_service),
):
    await service.register(data)

    background_tasks.add_task(
        email_service.send_welcome_email,
        data.username,
        data.email
    )

    return data.username


@router.post("/login")
async def login(
    data: LoginSchema,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(data)


@router.post("/refresh")
async def refresh(
    token: RefreshSchema,
    service: AuthService = Depends(get_auth_service),
):
    return await service.refresh(token.refresh_token)


@router.post("/logout")
async def logout(
    token: RefreshSchema,
    service: AuthService = Depends(get_auth_service),
):
    return await service.logout(token.refresh_token)


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return current_user
