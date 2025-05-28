from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from models.invoice import Invoice
from models.order import Order, OrderStatus
from models.user import User
from models.customer import Customer
from schemas.order import OrderOut, OrderListOut, OrderDetailOut, OrderFilteredOut, OrderFilter
from schemas.combined import OrderCreateCombined
from schemas.invoice import InvoiceListOut
from schemas.shipping import ShippingOrder
from utils.auth_dependency import get_current_user, get_db
from crud.order import crud_create_order, crud_get_orders, crud_filter_orders, crud_delete_order, crud_get_order_by_orderNumber, crud_update_order, crud_get_shipping_orders, crud_get_shipping_order_by_number

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



@router.get(
    "/filter/",
    response_model=List[OrderFilteredOut],
    summary="Filter Orders by Status and Customer Name",
    description="""
    Filter orders based on status and customer name.
    
    - **status**: Filter orders by their status (e.g., Pending, Delivered, Cancelled)
    - **customer_name**: Filter orders by customer name (matches partial names in first or last name)
    
    Returns a list of orders with the following fields:
    - invoice_number: Invoice number associated with the order
    - customer_name: Full name of the customer
    - order_date: Date when the order was placed
    - amount: Total amount of the order
    - payment_method: Payment method used for the order
    - status: Current status of the order
    """
)
async def filter_orders(
    filter_params: OrderFilter = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Filter orders based on status and customer name.
    
    Args:
        filter_params (OrderFilter): Parameters for filtering orders
        db (Session): Database session
        current_user (User): Current authenticated user
    
    Returns:
        List[OrderFilteredOut]: List of filtered orders
    
    Raises:
        HTTPException: If filtering fails
    """
    try:
        # Convert status to uppercase if provided
        status_value = filter_params.status.upper() if filter_params.status else None
        
        # Get orders with filtering
        query = db.query(Order).filter(Order.user_id == current_user.id)
        
        if status_value:
            query = query.filter(Order.status == status_value)
        
        if filter_params.customer_name:
            query = query.join(Customer, Order.customer_id == Customer.id)
            query = query.filter(
                Customer.first_name.ilike(f"%{filter_params.customer_name}%") |
                Customer.last_name.ilike(f"%{filter_params.customer_name}%")
            )
        
        # Execute query with proper loading
        orders = query.options(
            joinedload(Order.invoice),
            joinedload(Order.customer)
        ).all()
        
        # Prepare response
        result = []
        for order in orders:
            customer_name = f"{order.customer.first_name} {order.customer.last_name}" if order.customer else None
            result.append({
                "invoice_number": order.invoice.invoice_number if order.invoice else None,
                "customer_name": customer_name,
                "order_date": order.order_date,
                "amount": order.amount,
                "payment_method": order.payment_method,
                "status": order.status
            })
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to filter orders: {str(e)}"
        )

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
