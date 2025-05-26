from .base import BaseSchema
from .product import ProductOut

class OrderProductOut(BaseSchema):
    id: int
    product_id: int
    quantity: int
    discount: float
    subtotal: float
    product: ProductOut

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # Create a dictionary with the data
        data = {
            'id': obj.id,
            'product_id': obj.product_id,
            'quantity': obj.quantity,
            'discount': obj.discount,
            'subtotal': obj.subtotal,
            'product': ProductOut.from_orm(obj.product) if obj.product else None
        }
        return cls(**data)


class OrderProductCreate(BaseSchema):
    product_id: int
    quantity: int
    discount: float
    subtotal: float
