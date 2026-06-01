from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Users


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(select(Users).where(Users.id == user_id))

        return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        result = await self.session.execute(
            select(Users).where(Users.username == username)
        )

        return result.scalar_one_or_none()

    async def create(self, username: str, password: str):
        result = await self.session.execute(
            insert(Users)
            .values(username=username, password=password)
            .returning(Users.username)
        )

        user = result.scalar_one()
        return user
