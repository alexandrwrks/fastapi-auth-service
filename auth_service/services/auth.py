from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.repo.refresh_token_repo import RefreshTokenRepository
from auth_service.repo.users_repo import UserRepository
from auth_service.schemas import RegisterSchema, LoginSchema
from auth_service.services.password import HashingPassword
from security.hash.token import HashingToken
from security.jwt import JWTService


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
        refresh_repo: RefreshTokenRepository,
        jwt_service: JWTService,
    ):
        self.session = session
        self.user_repo = user_repo
        self.refresh_repo = refresh_repo
        self.jwt_service = jwt_service

    async def register(self, data: RegisterSchema):

        users = await self.user_repo.get_existing_user(data.username, data.email)

        for user in users:
            if user.username == data.username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this username already exists.",
                )

            if user.email == data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists.",
                )
        try:
            await self.user_repo.create(
                username=data.username,
                email=data.email,
                password=HashingPassword.hash_password(data.password),
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка регистрации пользователя"
            )

    async def login(self, data: LoginSchema):
        user = await self.user_repo.get_by_username(data.username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
            )

        if not HashingPassword.verify_password(user.password, data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )

        access_token = self.jwt_service.create_access_token(user.id, user.role)

        refresh_token = self.jwt_service.create_refresh_token(user.id, user.role)

        await self.refresh_repo.delete_by_id(user.id)

        await self.refresh_repo.create(
            user_id=user.id,
            token=HashingToken.hashing_token(refresh_token),
        )

        print(refresh_token)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh(self, refresh_token: str):
        payload = self.jwt_service.verify_refresh_token(refresh_token)

        user_id = int(payload["sub"])
        role = payload["role"]

        hash_db_token = await self.refresh_repo.get_by_id(user_id)

        db_token = HashingToken.check_token(refresh_token, hash_db_token.token)

        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found."
            )

        if hash_db_token.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is already revoked.",
            )

        new_access = self.jwt_service.create_access_token(user_id, role)

        new_refresh = self.jwt_service.create_refresh_token(user_id, role)


        await self.refresh_repo.delete_by_id(user_id)
        await self.refresh_repo.create(user_id, new_refresh)

        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }

    async def logout(self, refresh_token: str):
        token = await self.refresh_repo.get_by_token(refresh_token)

        if token:
            await self.refresh_repo.revoke(token.id)

        return {"message": "success"}
