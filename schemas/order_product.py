from .base import BaseSchema
from .product import ProductOut

class OrderProductOut(BaseSchema):
    id: int
    product_id: int
    quantity: int
    discount: float
    subtotal: float
    product: ProductOut


class OrderProductCreate(BaseSchema):
    product_id: int
    quantity: int
    discount: float
    subtotal: float
