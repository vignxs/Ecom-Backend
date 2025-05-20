from .base import BaseSchema
from datetime import datetime
from typing import Optional
from .customer import CustomerCreate
from models.order import OrderStatus

class InvoiceCreate(BaseSchema):
    invoice_number: str
    customer: CustomerCreate
    order_id: int
    amount: float
    status: OrderStatus = OrderStatus.PENDING
    issued_date: Optional[datetime] = None

class InvoiceUpdate(BaseSchema):
    invoice_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    amount: Optional[float] = None

    class Config:
        extra = 'allow'

class InvoiceListOut(BaseSchema):
    invoice: str
    customer_name: str
    issued_date: datetime
    amount: float
    status: str

    class Config:
        orm_mode = True
