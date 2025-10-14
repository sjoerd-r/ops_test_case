import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from decimal import Decimal

from core_wms.app.services.product.variant import ProductVariantService
from core_wms.app.services.product.variant.dto import ProductVariant, ProductVariantFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.product.main import Product

@strawberry.type
class ProductVariant:
    id: int | None = None
    product_id: int | None = None
    shopify_variant_id: int | None = None
    inventory_item_id: int | None = None
    sku: str | None = None
    barcode: str | None = None
    title: str | None = None
    option1: str | None = None
    option2: str | None = None
    option3: str | None = None
    price: Decimal | None = None
    compare_at_price: Decimal | None = None
    inventory_quantity: int | None = None
    weight: float | None = None
    weight_unit: str | None = None
    requires_shipping: bool | None = None
    taxable: bool | None = None
    position: int | None = None
    image_id: int | None = None
    available_for_sale: bool | None = None
    inventory_policy: str | None = None
    inventory_management: str | None = None
    fulfillment_service: str | None = None
    tax_code: str | None = None
    unit_price: Decimal | None = None
    unit_price_measurement: JSON | None = None  # type: ignore[misc]
    selected_options: JSON | None = None  # type: ignore[misc]
    metafields: JSON | None = None  # type: ignore[misc]
    legacy_resource_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def product(self, info, parent: strawberry.Parent["ProductVariant"]) -> Annotated["Product", strawberry.lazy("core_wms.app.graphql.schemas.product.main")] | None:
        return await info.context.loaders.product_variant.product.load(parent.product_id)

@strawberry.type
class ProductVariantQueries:
    @strawberry.field
    @staticmethod
    async def product_variants(info, id: int | None = None, product_id: int | None = None) -> List["ProductVariant"]:
        return await ProductVariantService(info.context.session).get_product_variants(
            ProductVariantFilter(id=id, product_id=product_id)
        )
        
    @strawberry.field
    @staticmethod
    async def product_variant(info, id: int) -> "ProductVariant" | None:
        return await ProductVariantService(info.context.session).get_product_variant(
            ProductVariantFilter(id=id)
        )

@strawberry.type
class ProductVariantMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_product_variant(
        info,
        product_id: int,
        id: int | None = None,
        shopify_variant_id: int | None = None,
        inventory_item_id: int | None = None,
        sku: str | None = None,
        barcode: str | None = None,
        title: str | None = None,
        option1: str | None = None,
        option2: str | None = None,
        option3: str | None = None,
        price: Decimal | None = None,
        compare_at_price: Decimal | None = None,
        inventory_quantity: int | None = None,
        weight: float | None = None,
        weight_unit: str | None = None,
        requires_shipping: bool | None = None,
        taxable: bool | None = None,
        position: int | None = None,
        image_id: int | None = None,
        available_for_sale: bool | None = None,
        inventory_policy: str | None = None,
        inventory_management: str | None = None,
        fulfillment_service: str | None = None,
        tax_code: str | None = None,
        unit_price: Decimal | None = None,
        unit_price_measurement: JSON | None = None,  # type: ignore[misc]
        selected_options: JSON | None = None,  # type: ignore[misc]
        metafields: JSON | None = None,  # type: ignore[misc]
        legacy_resource_id: int | None = None,
    ) -> "ProductVariant":
        return await ProductVariantService(info.context.session).upsert_product_variant(
            ProductVariant(
                id=id,
                product_id=product_id,
                shopify_variant_id=shopify_variant_id,
                inventory_item_id=inventory_item_id,
                sku=sku,
                barcode=barcode,
                title=title,
                option1=option1,
                option2=option2,
                option3=option3,
                price=price,
                compare_at_price=compare_at_price,
                inventory_quantity=inventory_quantity,
                weight=weight,
                weight_unit=weight_unit,
                requires_shipping=requires_shipping,
                taxable=taxable,
                position=position,
                image_id=image_id,
                available_for_sale=available_for_sale,
                inventory_policy=inventory_policy,
                inventory_management=inventory_management,
                fulfillment_service=fulfillment_service,
                tax_code=tax_code,
                unit_price=unit_price,
                unit_price_measurement=unit_price_measurement,
                selected_options=selected_options,
                metafields=metafields,
                legacy_resource_id=legacy_resource_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_product_variant(info, id: int) -> bool:
        return await ProductVariantService(info.context.session).delete_product_variant(
            ProductVariant(id=id)
        )

@strawberry.type
class ProductVariantSubscriptions:
    @strawberry.subscription
    async def product_variant_created(self, info) -> AsyncGenerator[ProductVariant, None]:
        yield

    @strawberry.subscription
    async def product_variant_updated(self, info) -> AsyncGenerator[ProductVariant, None]:
        yield

    @strawberry.subscription
    async def product_variant_deleted(self, info) -> AsyncGenerator[int, None]:
        yield