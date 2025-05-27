from sqlalchemy.orm import Session
from database import SessionLocal
from models.invoice import Invoice
from models.order import Order
from models.customer import Customer
from datetime import datetime
import random

def insert_default_invoices():
    db = SessionLocal()
    
    try:
        # Create some sample customers if they don't exist
        customers = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_country_code": "+1",
                "phone_number": "555-0123"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "phone_country_code": "+1",
                "phone_number": "555-0124"
            }
        ]

        # Get existing orders
        orders = db.query(Order).all()
        
        # Create invoices for existing orders
        for order in orders:
            # Get or create customer
            customer = db.query(Customer).filter(
                Customer.email == order.customer.email
            ).first()
            if not customer:
                customer = Customer(
                    first_name=order.customer.first_name,
                    last_name=order.customer.last_name,
                    email=order.customer.email,
                    phone_country_code=order.customer.phone_country_code,
                    phone_number=order.customer.phone_number
                )
                db.add(customer)
                db.commit()
                db.refresh(customer)

            # Create invoice
            invoice = Invoice(
                invoice_number=f"INV-{order.id:05d}",
                customer_name=f"{customer.first_name} {customer.last_name}",
                order_id=order.id,
                amount=order.amount,
                status=order.status,
                issued_date=order.order_date
            )
            db.add(invoice)

        db.commit()
        print("Default invoices created successfully!")
    
    except Exception as e:
        db.rollback()
        print(f"Error creating invoices: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_default_invoices()
