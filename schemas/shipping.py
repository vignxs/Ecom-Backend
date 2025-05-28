from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from models.customer import Customer
from models.address import Address
from models.order import OrderProduct
from models.product import Product

class ShippingOrder(BaseModel):
    id: int
    order_number: str
    order_date: datetime
    amount: float
    payment_method: str
    status: str
    customer: Customer
    shipping_address: Address
    order_products: List[OrderProduct]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }
