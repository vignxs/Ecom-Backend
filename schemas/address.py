from .base import BaseSchema
from typing import Optional

class AddressCreate(BaseSchema):
    building: Optional[str] = None
    apartment_no: Optional[str] = None
    house_no: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class AddressUpdate(BaseSchema):
    building: Optional[str] = None
    apartment_no: Optional[str] = None
    house_no: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class AddressOut(BaseSchema):
    building: Optional[str]
    apartment_no: Optional[str]
    house_no: Optional[str]
    street: Optional[str]
    city: Optional[str]
    country: Optional[str]

    class Config:
        orm_mode = True

