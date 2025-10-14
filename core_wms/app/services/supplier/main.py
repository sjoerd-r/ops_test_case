import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.suppliers import Supplier

logger = logging.getLogger(__name__)

@final
class SupplierService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_suppliers(self) -> List[Supplier]:
        try:
            result = await self.session.execute(select(Supplier))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_suppliers failed: {e}")
            raise

    async def upsert_supplier(self, args: dict) -> Supplier:
        try:
            supplier = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Supplier).where(Supplier.id == args['id'])
                )
                supplier = result.scalars().first()

            if supplier:
                for key, value in args.items():
                    if hasattr(supplier, key) and value is not None:
                        setattr(supplier, key, value)
            else:
                supplier = Supplier(**args)
                self.session.add(supplier)
            
            await self.session.commit()
            await self.session.refresh(supplier)
            return supplier
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_supplier failed: {e}")
            raise
    
    async def delete_supplier(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Supplier).where(Supplier.id == id)
            )
            supplier = result.scalars().first()

            if supplier:
                await self.session.delete(supplier)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_supplier failed: {e}")
            raise