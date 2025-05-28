from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from models.order import Order, OrderStatus
from models.user import User
from schemas.order import OrderDetailOut
from utils.auth_dependency import get_current_user, get_db
from crud.order import crud_get_order_by_orderNumber, crud_get_shipping_orders

router = APIRouter(prefix="/shipping", tags=["shipping"])

@router.get("/", response_model=List[OrderDetailOut])
async def list_shipping_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all shipping orders for the current user."""
    try:
        return crud_get_shipping_orders(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_number}", response_model=OrderDetailOut)
async def get_shipping_order(
    order_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get shipping details for a specific order."""
    try:
        order = crud_get_order_by_orderNumber(db, order_number, current_user.id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
