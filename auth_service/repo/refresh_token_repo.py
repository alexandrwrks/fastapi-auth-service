from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, token: str):
        await self.session.execute(
            insert(RefreshToken).values(user_id=user_id, token=token)
        )

    async def get_by_token(self, token: str):
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )

        return result.scalar_one_or_none()

    async def revoke(self, token_id: int):
        await self.session.execute(
            update(RefreshToken)
            .values(is_revoked=True)
            .where(RefreshToken.id == token_id)
        )

    async def delete_by_id(self, user_id: int):
        await self.session.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user_id)
        )

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.user_id == user_id)
        )

        return result.scalar_one_or_none()
