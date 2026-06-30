from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.repo.refresh_token_repo import RefreshTokenRepository
from auth_service.repo.users_repo import UserRepository
from auth_service.services.auth import AuthService
from db.config import get_async_session
from db.models.enums import Roles
from security.jwt import JWTService
from utils.config import settings


async def get_jwt_service() -> JWTService:
    return JWTService(settings)


async def get_user_repo(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return UserRepository(session)


async def get_auth_service(
    session: AsyncSession = Depends(get_async_session),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    return AuthService(
        session=session,
        user_repo=UserRepository(session=session),
        refresh_repo=RefreshTokenRepository(session=session),
        jwt_service=jwt_service,
    )


security = HTTPBearer()


async def get_http_security(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> HTTPAuthorizationCredentials:
    return credentials


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(get_http_security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    payload = jwt_service.verify_access_token(credentials.credentials)

    return payload


async def get_admin_user(
    payload: dict = Depends(get_current_user),
):
    if payload["role"] != Roles.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You dont have permission to perform this action",
        )

    return payload
