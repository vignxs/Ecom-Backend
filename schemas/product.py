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
    price: float
    stock_status: str
    quantity: int
    sku_no: str
    permalink: Optional[str]
    images: Optional[str]  # Could be changed to List[str] if stored as JSON
    content: Optional[str]
    status: str
    created_at: datetime

    class Config:
        form_attributes = True


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