from typing import List, Optional
from sqlalchemy.orm import Session
from crud.customer import create_customer
from models.order import Order, Customer, Address, OrderProduct
from models.product import Product
from models.order import Order, Customer, Address, OrderProduct, OrderStatus
from schemas.order import OrderCreate, OrderUpdate, OrderDetailOut
from models.invoice import Invoice
from schemas.combined import OrderCreateCombined
from datetime import datetime
from sqlalchemy.orm import joinedload

def crud_get_order_number(db: Session) -> str:
    """Generate a unique order number."""
    try:
               
        last_order = db.query(Order).order_by(Order.id.desc()).first()
        if last_order:
            last_id = last_order.id
        else:
            last_id = 0
        
        return f"ORD-{last_id + 1:05d}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise ValueError(f"Failed to generate order number: {str(e)}")

# Ensure OrderStatus is properly imported at the top of the file
from models.order import Order, Customer, Address, OrderProduct, OrderStatus

def crud_create_customer(db: Session, customer_data: dict) -> Customer:
    """Create a new customer if they don't exist."""
    try:
        customer = db.query(Customer).filter(Customer.email == customer_data['email']).first()
        if not customer:
            customer = Customer(**customer_data)
            db.add(customer)
            db.commit()
            db.refresh(customer)
        return customer
    except Exception as e:
        raise ValueError(f"Failed to create customer: {str(e)}")



def crud_create_order(db: Session, order_data: OrderCreateCombined, user_id: int) -> Order:
    """Create a new order with all related entities."""
    try:
        # Create or get customer
        customer = create_customer(db, order_data.customer)

        # Generate order number
        order_number = crud_get_order_number(db)



        # Create order
        order = Order(
            order_number=order_number,
            customer_id=customer.id,
            order_date=datetime.utcnow(),
            payment_method=order_data.payment_method,
            status=OrderStatus.PENDING,
            user_id=user_id,
            amount=0.0
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # Create shipping address
        shipping_address = Address(
            building=order_data.shipping_address.building,
            apartment_no=order_data.shipping_address.apartment_no,
            house_no=order_data.shipping_address.house_no,
            street=order_data.shipping_address.street,
            city=order_data.shipping_address.city,
            country=order_data.shipping_address.country,
            order_id=order.id
        )
        db.add(shipping_address)

        # Add products and calculate total
        total_amount = 0.0
        for item in order_data.products:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"Product id {item.product_id} not found")
            
            price = product.sale_price if product.sale_price is not None else product.regular_price
            subtotal = (price * item.quantity) - (item.discount or 0)
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
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise ValueError(f"Failed to create order: {str(e)}")

def crud_get_orders(db: Session, user_id: int) -> List[Order]:
    """Get all orders for a user."""
    try:
        return db.query(Order).filter(Order.user_id == user_id).all()
    except Exception as e:
        raise ValueError(f"Failed to fetch orders: {str(e)}")

def crud_filter_orders(db: Session, user_id: int, status: Optional[str] = None, customer_name: Optional[str] = None) -> List[Order]:
    """Filter orders based on status and customer name."""
    try:
        query = db.query(Order).filter(Order.user_id == user_id)
        if status:
            query = query.filter(Order.status == status)
        if customer_name:
            query = query.join(Customer).filter(
                (Customer.first_name.ilike(f"%{customer_name}%")) |
                (Customer.last_name.ilike(f"%{customer_name}%"))
            )
        return query.all()
    except Exception as e:
        raise ValueError(f"Failed to filter orders: {str(e)}")

def crud_update_order(db: Session, order_id: int, update_data: OrderUpdate, user_id: int) -> Order:
    """Update an existing order."""
    try:
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        if not order:
            raise ValueError("Order not found")
        
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(order, key, value)
        
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update order: {str(e)}")

from sqlalchemy.orm import joinedload

def crud_get_order_by_orderNumber(db: Session, order_number: str, user_id: int):
    """Get order details including all related models."""
    # Query with all necessary fields for serialization
    # Query the main order with all relationships
    order = db.query(Order).options(
        joinedload(Order.customer),
        joinedload(Order.shipping_address),
        joinedload(Order.order_products).joinedload(OrderProduct.product)
    ).filter(
        Order.order_number == order_number,
        Order.user_id == user_id
    ).first()

    if not order:
        return None

    return OrderDetailOut.from_orm(order)


def crud_delete_order(db: Session, order_id: int, user_id: int) -> None:
    """Delete an order and its related entities."""
    try:
        order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
        if not order:
            raise ValueError("Order not found")
        
        # Delete related entities
        db.query(OrderProduct).filter(OrderProduct.order_id == order_id).delete()
        db.query(Address).filter(Address.order_id == order_id).delete()
        db.delete(order)
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete order: {str(e)}")
