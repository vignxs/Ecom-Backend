from .base import BaseSchema
from .product import ProductOut

class OrderProductOut(BaseSchema):
    product: ProductOut
    quantity: int
    discount: float
    subtotal: float


class OrderProductCreate(BaseSchema):
    product_id: int
    quantity: int
    discount: float
    subtotal: float
