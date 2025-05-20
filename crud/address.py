from typing import Optional
from sqlalchemy.orm import Session
from models.address import Address
from schemas.address import AddressCreate, AddressUpdate

def create_address(db: Session, address_data: AddressCreate) -> Address:
    """Create a new address."""
    try:
        address = Address(**address_data.dict())
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create address: {str(e)}")

def get_address(db: Session, address_id: int) -> Optional[Address]:
    """Get an address by ID."""
    try:
        return db.query(Address).filter(Address.id == address_id).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch address: {str(e)}")

def get_address_by_order(db: Session, order_id: int) -> Optional[Address]:
    """Get address by order ID."""
    try:
        return db.query(Address).filter(Address.order_id == order_id).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch address: {str(e)}")

def update_address(db: Session, address_id: int, update_data: AddressUpdate) -> Address:
    """Update an existing address."""
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise ValueError("Address not found")
        
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(address, key, value)
        
        db.commit()
        db.refresh(address)
        return address
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update address: {str(e)}")

def delete_address(db: Session, address_id: int) -> None:
    """Delete an address."""
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise ValueError("Address not found")
        
        db.delete(address)
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete address: {str(e)}")
