import logging
from typing import TypeVar, Callable, Awaitable, Any

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

T = TypeVar('T')

class BaseService:
    """General base class for entity services.
    
    Provides transaction management and error handling with consistent session access patterns.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def execute(self, operation_name: str, func: Callable[[], Awaitable[T]]) -> T:
        try:
            result = await func()
            
            await self.session.commit()
            
            return result
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"{operation_name} failed: {e}")
            raise
    
    async def flush(self) -> None:
        await self.session.flush()
    
    async def refresh(self, obj: Any) -> None:
        await self.session.refresh(obj)
    
    async def add(self, obj: Any) -> None:
        self.session.add(obj)
    
    async def delete(self, obj: Any) -> None:
        await self.session.delete(obj)