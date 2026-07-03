from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.config import get_async_session


async def get_ai_service(
        session: AsyncSession = Depends(get_async_session),
):
    ...