from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, conint, constr
from typing import Optional, List

from .base import BaseSchema

class ProductOrderCreate(BaseSchema):
    product_id: int
    quantity: int
    discount: Optional[float] = 0.0

class ProductOut(BaseSchema):
    id: int
    product_name: str
    description: Optional[str]
    regular_price: float
    stock_status: str
    stock_quantity: int
    sku: Optional[str] = None
    permalink: str
    image: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = 'active'
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            product_name=obj.product_name,
            description=obj.description,
            regular_price=obj.regular_price,
            stock_status=obj.stock_status,
            stock_quantity=obj.stock_quantity,
            sku=obj.sku,
            permalink=obj.permalink,
            image=obj.image,
            content=obj.description if obj.description else None,
            status='active',
            created_at=obj.created_at
        )

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            product_name=obj.product_name,
            description=obj.description,
            price=obj.regular_price,
            stock_status=obj.stock_status,
            quantity=obj.stock_quantity,
            sku_no=obj.sku,
            permalink=obj.permalink,
            image=obj.image,
            content=obj.description,
            status='active',
            created_at=obj.created_at
        )


class ProductCreate(BaseModel):
    product_name: constr(min_length=1)
    permalink: constr(min_length=1)
    description: Optional[str] = None
    product_code: Optional[str] = None
    sku: Optional[str] = None
    gtin_upc_ean_isbn: Optional[str] = None
    tax: Optional[float] = 0.0
    stock_quantity: Optional[int] = 0
    stock_status: Optional[str] = "In Stock"
    low_stock_threshold: Optional[int] = 0
    allow_backorder: Optional[bool] = False
    brand: Optional[str] = None
    collection: Optional[str] = None
    regular_price: float
    sale_price: Optional[float] = None
    shipping_charges: Optional[float] = 0.0
    weight: Optional[float] = 0.0
    length: Optional[float] = 0.0
    width: Optional[float] = 0.0
    height: Optional[float] = 0.0
    seo_title: Optional[str] = None
    seo_keywords: Optional[str] = None
    seo_description: Optional[str] = None
    product_status: Optional[str] = "Draft"
    is_featured: Optional[bool] = False

    # For tags, categories, attributes, faqs you can add lists here

ProductUpdate = ProductCreate