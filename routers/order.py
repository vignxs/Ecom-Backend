from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from models.order import Invoice, Order, OrderStatus
from models.user import User
from schemas.order import InvoiceListOut, OrderCreate, OrderListOut, OrderOut, OrderUpdate
from utils.auth_dependency import get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.order import Order, Customer, Address, Product, OrderProduct
from schemas.order import OrderCreate, OrderOut  # Define OrderOut schema as needed
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def generate_order_number(db: Session):
    # Simple example, use better logic in prod
    last_order = db.query(Order).order_by(Order.id.desc()).first()
    last_id = last_order.id if last_order else 0
    return f"ORD-{last_id + 1:05d}"

@router.post("/orders/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if customer exists by email, else create
    customer = db.query(Customer).filter(Customer.email == order_in.customer.email).first()
    if not customer:
        customer = Customer(
            first_name=order_in.customer.first_name,
            last_name=order_in.customer.last_name,
            email=order_in.customer.email,
            phone_country_code=order_in.customer.phone_country_code,
            phone_number=order_in.customer.phone_number
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # Generate order number
    order_number = generate_order_number(db)

    order = Order(
        order_number=order_number,
        customer_id=customer.id,
        order_date=datetime.utcnow(),
        payment_method=order_in.payment_method,
        status="Pending",
        user_id=current_user.id,
        amount=0.0  # will calculate below
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Add shipping address
    shipping_address = Address(
        building=order_in.shipping_address.building,
        apartment_no=order_in.shipping_address.apartment_no,
        house_no=order_in.shipping_address.house_no,
        street=order_in.shipping_address.street,
        city=order_in.shipping_address.city,
        country=order_in.shipping_address.country,
        order_id=order.id
    )
    db.add(shipping_address)

    # Calculate total amount from products
    total_amount = 0.0
    for item in order_in.products:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product id {item.product_id} not found")
        
        subtotal = (product.price * item.quantity) - (item.discount or 0)
        if subtotal < 0:
            subtotal = 0
        
        order_product = OrderProduct(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            discount=item.discount or 0,
            subtotal=subtotal
        )
        db.add(order_product)
        total_amount += subtotal

    order.amount = total_amount
    db.commit()
    db.refresh(order)

    return order


@router.get("/", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/filter", response_model=List[OrderOut])
def filter_orders(
    status: Optional[str] = Query(None, description="Order status (Pending, Delivered, etc)"),
    customer_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Order).filter(Order.user_id == current_user.id)

    if status:
        try:
            # Convert to Enum (raise ValueError if invalid)
            status_enum = OrderStatus(status.capitalize())
            query = query.filter(Order.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status '{status}'")

    if customer_name:
        query = query.filter(Order.customer_name.ilike(f"%{customer_name}%"))

    return query.all()

@router.put("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(db_order, field, value)

    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}

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


@router.get("/orders/{order_id}", response_model=OrderDetailOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order