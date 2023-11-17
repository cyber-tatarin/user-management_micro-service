from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.postgres_repository import UserRepository, async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)