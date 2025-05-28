from .base import BaseSchema
from typing import Optional, List
from datetime import datetime
from .customer import CustomerOut
from .address import AddressOut
from .order_product import OrderProductOut
from .invoice import InvoiceListOut
from models.order import OrderStatus
from .product import ProductOut 
from pydantic import BaseModel




class OrderProductOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True 


class OrderBase(BaseSchema):
    customer_name: str
    amount: float
    payment_method: str
    status: Optional[str] = OrderStatus.PENDING

class OrderCreate(OrderBase):
    order_number: str

class OrderUpdate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_number: str
    order_date: datetime
    created_at: datetime
    updated_at: datetime

class OrderOut(BaseSchema):
    id: int
    order_number: str
    customer_id: int
    order_date: datetime
    amount: float
    payment_method: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class OrderListOut(BaseSchema):
    invoice: str
    customer_name: str
    order_date: datetime
    amount: float
    payment_method: str
    status: OrderStatus

    class Config:
        from_attributes = True

class OrderFilteredOut(BaseSchema):
    invoice_number: Optional[str]
    customer_name: str
    order_date: datetime
    amount: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True

class OrderFilter(BaseSchema):
    """Schema for filtering orders.
    
    Attributes:
        status (Optional[str]): Order status to filter by (e.g., 'Pending', 'Delivered')
        customer_name (Optional[str]): Customer name to filter by (matches partial names in first or last name)
    """
    status: Optional[str] = None
    customer_name: Optional[str] = None

    class Config:
        """Pydantic configuration.
        
        Attributes:
            orm_mode (bool): Enable ORM mode for model conversion
        """
        orm_mode = True

class OrderDetailOut(BaseSchema):
    id: int
    order_number: str
    order_date: datetime
    amount: float
    payment_method: Optional[str]
    status: OrderStatus
    customer: CustomerOut
    shipping_address: Optional[AddressOut]
    order_products: List[OrderProductOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
