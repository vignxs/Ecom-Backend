from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False)
    permalink = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    product_code = Column(String(100), nullable=True)
    sku = Column(String(100), nullable=True)
    gtin_upc_ean_isbn = Column(String(100), nullable=True)
    tax = Column(Float, default=0.0)
    stock_quantity = Column(Integer, default=0)
    stock_status = Column(String(50), default="In Stock")  # you can make this Enum
    low_stock_threshold = Column(Integer, default=0)
    allow_backorder = Column(Boolean, default=False)
    brand = Column(String(100), nullable=True)
    collection = Column(String(100), nullable=True)
    regular_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=True)
    shipping_charges = Column(Float, default=0.0)
    weight = Column(Float, default=0.0)
    length = Column(Float, default=0.0)
    width = Column(Float, default=0.0)
    height = Column(Float, default=0.0)
    seo_title = Column(String(255), nullable=True)
    seo_keywords = Column(String(255), nullable=True)
    seo_description = Column(Text, nullable=True)
    product_status = Column(String(50), default="Draft")  # Draft, Published, etc.
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # For categories, tags, attributes, faqs — you can create related tables and setup relationships.
