from typing import Optional
from sqlalchemy.orm import Session
from models.order_product import OrderProduct
from schemas.order_product import OrderProductCreate

def create_order_product(db: Session, order_product_data: OrderProductCreate) -> OrderProduct:
    """Create a new order product."""
    try:
        order_product = OrderProduct(**order_product_data.dict())
        db.add(order_product)
        db.commit()
        db.refresh(order_product)
        return order_product
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create order product: {str(e)}")

# def get_order_product(db: Session, order_product_id: int) -> Optional[OrderProduct]:
#     """Get an order product by ID."""
#     try:
#         return db.query(OrderProduct).filter(OrderProduct.id == order_product_id).first()
#     except Exception as e:
#         raise ValueError(f"Failed to fetch order product: {str(e)}")

# def get_order_products_by_order(db: Session, order_id: int) -> list[OrderProduct]:
#     """Get all order products for an order."""
#     try:
#         return db.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()
#     except Exception as e:
#         raise ValueError(f"Failed to fetch order products: {str(e)}")

# def update_order_product(db: Session, order_product_id: int, update_data: OrderProductUpdate) -> OrderProduct:
#     """Update an existing order product."""
#     try:
#         order_product = db.query(OrderProduct).filter(OrderProduct.id == order_product_id).first()
#         if not order_product:
#             raise ValueError("Order product not found")
        
#         for key, value in update_data.dict(exclude_unset=True).items():
#             setattr(order_product, key, value)
        
#         db.commit()
#         db.refresh(order_product)
#         return order_product
#     except Exception as e:
#         db.rollback()
#         raise ValueError(f"Failed to update order product: {str(e)}")

# def delete_order_product(db: Session, order_product_id: int) -> None:
#     """Delete an order product."""
#     try:
#         order_product = db.query(OrderProduct).filter(OrderProduct.id == order_product_id).first()
#         if not order_product:
#             raise ValueError("Order product not found")
        
#         db.delete(order_product)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise ValueError(f"Failed to delete order product: {str(e)}")
