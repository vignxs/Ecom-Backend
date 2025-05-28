from fastapi import Depends
from sqlalchemy.orm import Session
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
from models.order import Order, OrderStatus
from models.user import User
from schemas.combined import OrderCreateCombined
from schemas.customer import CustomerCreate
from schemas.address import AddressCreate
from schemas.product import ProductOrderCreate
from crud.order import crud_create_order
from datetime import datetime

# Create all tables if they don't exist
from models import Base
Base.metadata.create_all(bind=engine)

def create_test_orders():
    # Create a database session
    db = SessionLocal()
    
    try:
        # Get a test user (you might need to adjust this based on your actual user data)
        test_user = db.query(User).first()
        if not test_user:
            print("No user found in the database. Please create a user first.")
            return
        
        # Create 5 cancelled test orders
        for i in range(5):
            order_data = OrderCreateCombined(
                customer=CustomerCreate(
                    name=f"Test Customer {i}",
                    email=f"test{i}@example.com",
                    phone="1234567890"
                ),
                shipping_address=AddressCreate(
                    building=f"Building {i}",
                    apartment_no=f"Apt {i}",
                    house_no=f"House {i}",
                    street="Test Street",
                    city="Test City",
                    country="Test Country"
                ),
                products=[
                    ProductOrderCreate(
                        product_id=1,  # Adjust this based on your actual product IDs
                        quantity=2,
                        discount=0
                    )
                ],
                payment_method="Credit Card"
            )
            
            # Create the order
            order = crud_create_order(db, order_data, test_user.id)
            
            # Update the order status to Cancelled
            order.status = OrderStatus.CANCELLED
            db.commit()
            
            print(f"Created cancelled test order {i+1} with order number: {order.order_number}")
            
    except Exception as e:
        db.rollback()
        print(f"Error creating test orders: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_orders()
