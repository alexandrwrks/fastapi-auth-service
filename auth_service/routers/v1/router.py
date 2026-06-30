from fastapi import APIRouter, Depends

from auth_service.schemas import LoginSchema, RefreshSchema, RegisterSchema
from auth_service.services.auth import AuthService
from deps import get_auth_service, get_current_user

router = APIRouter(prefix="/auth_service", tags=["auth_service"])

"""
router  v1/auth_srvice
"""


@router.post("/register")
async def register(
    data: RegisterSchema,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register(data)


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
