import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.channels import Channel

logger = logging.getLogger(__name__)

@final
class ChannelService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_channels(self) -> List[Channel]:
        try:
            result = await self.session.execute(select(Channel))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_channels failed: {e}")
            raise

    async def upsert_channel(self, args: dict) -> Channel:
        try:
            channel = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Channel).where(Channel.id == args['id'])
                )
                channel = result.scalars().first()
            
            if channel:
                for key, value in args.items():
                    if hasattr(channel, key) and value is not None:
                        setattr(channel, key, value)
            else:
                channel = Channel(**args)
                self.session.add(channel)
            
            await self.session.commit()
            await self.session.refresh(channel)
            return channel
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_channel failed: {e}")
            raise
    
    async def delete_channel(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Channel).where(Channel.id == id)
            )
            channel = result.scalars().first()

            if channel:
                await self.session.delete(channel)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_channel failed: {e}")
            raise