import logging
from typing import List, Dict, Any
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.customers import Customer
from core_wms.app.services.customer.address import CustomerAddressService

logger = logging.getLogger(__name__)

async def _process_customer_related_entities(session: AsyncSession, customer_id: int, data: Dict[str, Any]) -> None:
    address_service = CustomerAddressService(session)
    
    addresses = data.get("addresses", [])
    for address in addresses:
        await address_service.upsert_customer_address({
            **address,
            "customer_id": customer_id,
            "shopify_address_id": address.get("id"),
            "shopify_customer_id": address.get("customer_id"),
        })
    
    default_address = data.get("default_address")
    if default_address:
        await address_service.upsert_customer_address({
            **default_address,
            "customer_id": customer_id,
            "shopify_address_id": default_address.get("id"),
            "shopify_customer_id": default_address.get("customer_id"),
            "default": True,
        })

@final
class CustomerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_customers(self) -> List[Customer]:
        try:
            result = await self.session.execute(select(Customer))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_customers failed: {e}")
            raise

    async def upsert_customer(self, data: Dict[str, Any], store_id: int) -> Customer:
        if store_id is None:
            raise ValueError("store_id is required")

        args = {**data, "store_id": store_id}
        
        if "shopify_customer_id" not in args and "id" in data:
            args["shopify_customer_id"] = data["id"]
            
        if not args.get("shopify_customer_id"):
            raise ValueError("shopify_customer_id is required")

        try:
            result = await self.session.execute(
                select(Customer).where(
                    Customer.store_id == store_id,
                    Customer.shopify_customer_id == args["shopify_customer_id"],
                )
            )
            customer = result.scalars().first()
            
            if customer:
                for key, value in args.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
            else:
                customer = Customer(**args)
                self.session.add(customer)

            await self.session.commit()
            await self.session.refresh(customer)
            
            await _process_customer_related_entities(self.session, customer.id, data)
            
            return customer
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_customer failed: {e}")
            raise

    async def delete_customer(self, store_id: int, shopify_customer_id: int) -> bool:
        if store_id is None or shopify_customer_id is None:
            raise ValueError("store_id and shopify_customer_id are required")
            
        try:
            result = await self.session.execute(
                select(Customer).where(
                    Customer.store_id == store_id,
                    Customer.shopify_customer_id == shopify_customer_id,
                )
            )
            customer = result.scalars().first()
            
            if not customer:
                return False
                
            await self.session.delete(customer)
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_customer failed: {e}")
            raise