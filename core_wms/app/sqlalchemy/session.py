from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlmodel import Session
from typing import AsyncGenerator

from core_wms.app.config.settings import settings as get_settings

class DatabaseSession:
    """General base class for session manager

    We provide a synchronous session from SQLModel, and an asynchronous session from SQLAlchemy's AsyncIO extension.

    NOTE: We want to keep session lifecycle at the edges (context, tasks, workers), not inside services, they should continue
    to receive an AsyncSession via dependency injection.
    """
    
    def __init__(self):
        settings = get_settings()
        self.async_engine = create_async_engine(
            settings.database.database_url,
            pool_pre_ping=True,
            echo=settings.database.debug,
        )
        sync_url = settings.database.database_url.replace("postgresql+asyncpg:", "postgresql:")
        self.sync_engine = create_engine(
            sync_url,
            pool_pre_ping=True,
            echo=settings.database.debug,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    def get_sync_session(self) -> Session:
        return Session(self.sync_engine)

db = DatabaseSession()