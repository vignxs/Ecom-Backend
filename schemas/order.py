from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class OrderStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderBase(BaseModel):
    customer_name: str
    amount: float
    payment_method: str
    status: Optional[str] = "Pending"

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

    class Config:
        form_attributes = True

class OrderOut(BaseModel):
    id: int
    order_number: str
    customer_name: str
    order_date: datetime
    amount: float
    payment_method: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        form_attributes = True    

class OrderListOut(BaseModel):
    invoice: str
    customer_name: str
    order_date: datetime
    amount: float
    payment_method: str
    status: OrderStatus

    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_country_code: Optional[str]
    phone_number: Optional[str]

class AddressCreate(BaseModel):
    building: Optional[str]
    apartment_no: Optional[str]
    house_no: Optional[str]
    street: Optional[str]
    city: Optional[str]
    country: Optional[str]

class ProductOrderCreate(BaseModel):
    product_id: int
    quantity: int
    discount: Optional[float] = 0.0

class OrderCreate(BaseModel):
    customer: CustomerCreate
    shipping_address: AddressCreate
    products: List[ProductOrderCreate]
    payment_method: str

class ProductOut(BaseModel):
    product_id: int
    quantity: int
    discount: float
    subtotal: float

class AddressOut(BaseModel):
    building: Optional[str]
    apartment_no: Optional[str]
    house_no: Optional[str]
    street: Optional[str]
    city: Optional[str]
    country: Optional[str]

class CustomerOut(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_country_code: Optional[str]
    phone_number: Optional[str]

class OrderOut(BaseModel):
    id: int
    order_number: str
    customer: CustomerOut
    shipping_address: AddressOut
    order_products: List[ProductOut]
    amount: float
    payment_method: str
    status: str
    order_date: datetime

    class Config:
        orm_mode = True

class InvoiceListOut(BaseModel):
    invoice: str
    customer_name: str
    issued_date: datetime
    amount: float
    status: str

    class Config:
        orm_mode = True

class OrderProductOut(BaseModel):
    product: ProductOut
    quantity: int
    discount: float
    subtotal: float

    class Config:
        orm_mode = True
class OrderDetailOut(BaseModel):
    id: int
    order_number: str
    order_date: datetime
    amount: float
    payment_method: Optional[str]
    status: str
    customer: CustomerOut
    shipping_address: Optional[AddressOut]
    order_products: List[OrderProductOut]

    class Config:
        orm_mode = True