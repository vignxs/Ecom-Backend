from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.invoice import Invoice
from models.order import Order, OrderStatus
from models.user import User
from utils.database import get_db
from utils.auth import create_user
from schemas.user import UserCreate

def create_default_invoices(db: Session):
    """Create default invoice data for testing."""
    try:
        # Create a test user if it doesn't exist
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            user_create = UserCreate(
                email="test@example.com",
                password="test123",
                first_name="Test",
                last_name="User"
            )
            test_user = create_user(db, user_create)

        # Create sample orders for the test user
        sample_orders = [
            {
                "order_number": "ORD-00001",
                "amount": 150.00,
                "payment_method": "Credit Card",
                "status": "Delivered",
                "order_date": datetime.now() - timedelta(days=30)
            },
            {
                "order_number": "ORD-00002",
                "amount": 299.99,
                "payment_method": "Cash on Delivery",
                "status": "Pending",
                "order_date": datetime.now() - timedelta(days=14)
            },
            {
                "order_number": "ORD-00003",
                "amount": 45.50,
                "payment_method": "Bank Transfer",
                "status": "Cancelled",
                "order_date": datetime.now() - timedelta(days=7)
            }
        ]

        # Create invoices for each sample order
        for i, order_data in enumerate(sample_orders, 1):
            # Create order
            order = Order(
                order_number=order_data["order_number"],
                amount=order_data["amount"],
                payment_method=order_data["payment_method"],
                status=order_data["status"],
                order_date=order_data["order_date"],
                user_id=test_user.id
            )
            db.add(order)
            db.flush()  # Get order ID

            # Create invoice
            invoice = Invoice(
                invoice_number=f"INV-{i:05d}",
                order_id=order.id,
                amount=order_data["amount"],
                issued_date=order_data["order_date"],
                due_date=order_data["order_date"] + timedelta(days=7),
                status="Paid" if order_data["status"] == "Delivered" else "Unpaid",
                payment_method=order_data["payment_method"]
            )
            db.add(invoice)

        db.commit()
        print("Default invoices created successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error creating default invoices: {str(e)}")
        raise

if __name__ == "__main__":
    # Get database session
    db = next(get_db())
    
    # Create default invoices
    create_default_invoices(db)
    
    # Close the database session
    db.close()
