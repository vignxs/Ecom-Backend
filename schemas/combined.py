from .base import BaseSchema
from .customer import CustomerCreate, CustomerOut
from .address import AddressCreate, AddressOut
from .product import ProductOrderCreate, ProductOut
from .order_product import OrderProductOut
from typing import List, Optional
from datetime import datetime

class OrderCreateCombined(BaseSchema):
    customer: CustomerCreate
    shipping_address: AddressCreate
    products: List[ProductOrderCreate]
    payment_method: str

class OrderDetailOut(BaseSchema):
    id: int
    order_number: str
    order_date: datetime
    amount: float
    payment_method: Optional[str]
    status: str
    customer: CustomerOut
    shipping_address: Optional[AddressOut]
    order_products: List[OrderProductOut]
