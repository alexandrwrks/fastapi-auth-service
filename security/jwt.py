from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status

from utils.config import Settings, settings


class JWTService:
    def __init__(self, setting: Settings):
        self.SECRET_KEY = setting.SECRET_KEY
        self.ALGORITHM = setting.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = setting.REFRESH_TOKEN_EXPIRE_DAYS

    def create_access_token(self, user_id: int, role: str):
        now = datetime.now(UTC)

        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "role": role,
            "exp": now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def create_refresh_token(self, user_id: int, role: str):
        now = datetime.now(UTC)

        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "iat": now,
            "role": role,
            "exp": now + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS),
        }

        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_token(self, token: str):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

    def verify_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[self.ALGORITHM],
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired",
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
            )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload

    def verify_refresh_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[self.ALGORITHM],
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload
