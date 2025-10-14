from decimal import Decimal
from typing import Dict, Any
from pydantic import BaseModel, Field, model_validator

class Product(BaseModel):
    model_config = {"from_attributes": True}
    
    store_id: int = Field(..., description="Store ID")
    shopify_product_id: int = Field(..., description="Shopify Product ID")
    title: str | None = Field(None, description="Product title")
    body_html: str | None = Field(None, description="Product description in HTML format")
    vendor: str | None = Field(None, description="Product vendor name")
    product_type: str | None = Field(None, description="Product type or category")
    handle: str | None = Field(None, description="URL-friendly product identifier")
    tags: str | None = Field(None, description="Comma-separated list of product tags")
    
    @model_validator(mode='before')
    @classmethod
    def transform_shopify_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(data, dict) and "id" in data and "shopify_product_id" not in data:
            data["shopify_product_id"] = data["id"]
        return data
    
    @classmethod
    def from_shopify(cls, data: Dict[str, Any], store_id: int) -> "Product":
        return cls.model_validate(data | {"store_id": store_id})

class ProductFilter(BaseModel):
    store_id: int = Field(..., description="Store ID")
    shopify_product_id: int | None = Field(None, description="Shopify Product ID to filter by")

class ProductVariant(BaseModel):
    model_config = {"from_attributes": True}
    
    product_id: int = Field(..., description="Product ID")
    shopify_variant_id: int = Field(..., description="Shopify Variant ID") 
    title: str | None = Field(None, description="Variant title")
    price: Decimal | None = Field(None, description="Variant price")
    sku: str | None = Field(None, description="Stock keeping unit")
    position: int | None = Field(None, description="Display position order")
    
    @classmethod
    def from_shopify(cls, data: Dict[str, Any], product_id: int) -> "ProductVariant":
        return cls.model_validate(data | {"product_id": product_id, "shopify_variant_id": data.get("id")})

class ProductOption(BaseModel):
    model_config = {"from_attributes": True}
    
    product_id: int = Field(..., description="Product ID")
    shopify_option_id: int = Field(..., description="Shopify Option ID")
    name: str | None = Field(None, description="Option name (e.g., 'Size', 'Color')")
    position: int | None = Field(None, description="Display position order")
    values: list[str] | None = Field(default_factory=list, description="Possible option values")
    
    @classmethod
    def from_shopify(cls, data: Dict[str, Any], product_id: int) -> "ProductOption":
        return cls.model_validate(data | {"product_id": product_id, "shopify_option_id": data.get("id")})

class ProductMedia(BaseModel):
    model_config = {"from_attributes": True}
    
    product_id: int = Field(..., description="Product ID")
    shopify_media_id: int = Field(..., description="Shopify Media ID")
    position: int | None = Field(None, description="Display position order")
    alt: str | None = Field(None, description="Alternative text for accessibility")
    width: int | None = Field(None, description="Image width in pixels")
    height: int | None = Field(None, description="Image height in pixels")
    src: str | None = Field(None, description="Media source URL")
    
    @classmethod
    def from_shopify(cls, data: Dict[str, Any], product_id: int) -> "ProductMedia":
        return cls.model_validate(data | {"product_id": product_id, "shopify_media_id": data.get("id")})

class ProductRelations(BaseModel):
    variants: list[ProductVariant] = Field(default_factory=list, description="Product variants")
    options: list[ProductOption] = Field(default_factory=list, description="Product options")
    media: list[ProductMedia] = Field(default_factory=list, description="Product media items")
    
    @classmethod
    def from_shopify(cls, data: Dict[str, Any], product_id: int) -> "ProductRelations":
        variants = [
            ProductVariant.from_shopify(variant, product_id)
            for variant in data.get("variants", [])
        ]
        
        options = [
            ProductOption.from_shopify(option, product_id)
            for option in data.get("options", [])
        ]
        
        media = [
            ProductMedia.from_shopify(media, product_id)
            for media in data.get("media", [])
        ]
        
        return cls(
            variants=variants,
            options=options,
            media=media
        )