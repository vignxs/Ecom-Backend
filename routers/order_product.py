from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.order_product import OrderProduct
from schemas.order_product import OrderProductOut
from utils.auth_dependency import get_current_user, get_db
from crud.order_product import create_order_product
from models.user import User

router = APIRouter(prefix="/order-products", tags=["order-products"])

@router.post("/", response_model=OrderProductOut, status_code=201)
async def create_order_product_endpoint(
    order_product_in: OrderProductOut,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order product."""
    try:
        return create_order_product(db, order_product_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/{order_product_id}", response_model=OrderProductOut)
# async def get_order_product_endpoint(
#     order_product_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """Get order product by ID."""
#     try:
#         return get_order_product(db, order_product_id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))

# @router.put("/{order_product_id}", response_model=OrderProductOut)
# async def update_order_product_endpoint(
#     order_product_id: int,
#     order_product_update: OrderProductOut,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """Update order product information."""
#     try:
#         return update_order_product(db, order_product_id, order_product_update)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/{order_product_id}")
# async def delete_order_product_endpoint(
#     order_product_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     """Delete order product."""
#     try:
#         delete_order_product(db, order_product_id)
#         return {"message": "Order product deleted successfully"}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
