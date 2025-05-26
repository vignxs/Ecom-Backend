from typing import Optional
from sqlalchemy.orm import Session
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate
from models.user import User

def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
    """Create a new customer."""
    try:
        existing = db.query(Customer).filter(Customer.email == customer_data.email).first()
        if existing:
            return existing
        
        customer = Customer(**customer_data.dict())
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create customer: {str(e)}")

def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    """Get a customer by ID."""
    try:
        return db.query(Customer).filter(Customer.id == customer_id).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch customer: {str(e)}")

def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    """Get a customer by email."""
    try:
        return db.query(Customer).filter(Customer.email == email).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch customer: {str(e)}")

def update_customer(db: Session, customer_id: int, update_data: CustomerUpdate) -> Customer:
    """Update an existing customer."""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(customer, key, value)
        
        db.commit()
        db.refresh(customer)
        return customer
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update customer: {str(e)}")

def delete_customer(db: Session, customer_id: int) -> None:
    """Delete a customer."""
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        
        db.delete(customer)
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete customer: {str(e)}")
