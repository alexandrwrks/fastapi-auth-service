from typing import List

from sqlalchemy import insert, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import Users


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(select(Users).where(Users.id == user_id))

        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Users | None:
        result = await self.session.execute(
            select(Users).where(Users.username == username)
        )

        return result.scalar_one_or_none()

    async def create(self, username: str, email: str, password: str):
        await self.session.execute(
            insert(Users)
            .values(
                username=username,
                email=email,
                password=password
            )
        )

    async def get_existing_user(self, username: str, email: str) -> List[Users]:
        result = await self.session.execute(
            select(Users)
            .where(
                or_(
                    (Users.username == username),
                    (Users.email == email)
                )
            )
        )

        return list(result.scalars().all())