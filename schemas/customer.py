from .base import BaseSchema
from pydantic import EmailStr
from typing import Optional

class CustomerCreate(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr
    phone_country_code: Optional[str] = None
    phone_number: Optional[str] = None

class CustomerOut(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr
    phone_country_code: Optional[str]
    phone_number: Optional[str]

    class Config:
        from_attributes = True

CustomerUpdate = CustomerCreate