from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import get_config
from src.auth import models

import os
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv

load_dotenv('.env')

settings = get_config(os.getenv("CONFIG"))


DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id) -> Optional[object]:
        raise NotImplementedError


class UserRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def add(self, entity):
        async with self.session as session:
            session.add(entity)
            await session.commit()
    
    async def get_by_id(self, entity_id) -> Optional[object]:
        async with self.session as session:
            user = await session.get(models.User, entity_id)
            return user
            
    async def get_by_email(self, email) -> Optional[models.User]:
        async with self.session as session:
            user = await session.execute(select(models.User).where(models.User.email == email))
            return user.scalar_one_or_none()

