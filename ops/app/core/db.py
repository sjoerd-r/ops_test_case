from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from ops.app.core.settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = (
    async_sessionmaker(engine, class_=SQLModelAsyncSession, expire_on_commit=False)
    if engine
    else None
)
