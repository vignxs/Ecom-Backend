from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.invoice import Invoice
from models.order import Order, OrderStatus
from models.user import User
from schemas.order import OrderOut, OrderListOut, OrderDetailOut
from schemas.combined import OrderCreateCombined
from schemas.invoice import InvoiceListOut
from utils.auth_dependency import get_current_user, get_db
from crud.order import crud_create_order, crud_get_orders,crud_filter_orders,crud_delete_order,crud_get_order_by_orderNumber,crud_update_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut, status_code=201)
async def create_order(
    order_in: OrderCreateCombined,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order."""
    try:
        result =  crud_create_order(db, order_in, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[OrderOut])
async def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all orders for the current user."""
    try:
        return crud_get_orders(db, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/", response_model=List[OrderOut])
async def filter_orders_endpoint(
    status: Optional[str] = Query(None, description="Order status (Pending, Delivered, etc)"),
    customer_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Filter orders based on status and customer name."""
    try:
        return crud_filter_orders(db, current_user.id, status, customer_name)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}", response_model=OrderOut)
async def update_order_endpoint(
    order_id: int,
    order_update: OrderCreateCombined,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing order."""
    try:
        return crud_update_order(db, order_id, order_update, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{order_id}")
async def delete_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an order."""
    try:
        crud_delete_order(db, order_id, current_user.id)
        return {"message": "Order deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list", response_model=List[OrderListOut])
def get_order_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = [
        OrderListOut(
            invoice=order.order_number,
            customer_name=order.customer.first_name + " " + order.customer.last_name,
            order_date=order.created_at,
            amount=order.total,
            payment_method=order.payment_method,
            status=order.status
        )
        for order in orders
    ]
    return result

@router.get("/shippings/list", response_model=List[OrderListOut])
def get_order_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = [
        OrderListOut(
            invoice=order.order_number,
            customer_name=order.customer.first_name + " " + order.customer.last_name,
            order_date=order.created_at,
            amount=order.total,
            payment_method=order.payment_method,
            status=order.status
        )
        for order in orders
    ]
    return result

@router.get("/invoices/list", response_model=List[InvoiceListOut])
def get_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
):
    invoices = (
        db.query(Invoice)
        .order_by(Invoice.issued_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        InvoiceListOut(
            invoice=invoice.invoice_number,
            customer_name=invoice.customer_name,  # stored directly
            issued_date=invoice.issued_date,
            amount=invoice.amount,
            status=invoice.status,
        )
        for invoice in invoices
    ]


@router.get("/{order_number}", response_model=OrderDetailOut)
def get_order(
    order_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = crud_get_order_by_orderNumber(db, order_number, current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
