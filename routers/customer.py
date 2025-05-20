from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerOut
from utils.auth_dependency import get_current_user, get_db
from crud.customer import create_customer, get_customer, update_customer, delete_customer
from models.user import User

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerOut, status_code=201)
async def create_customer_endpoint(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new customer."""
    try:
        return create_customer(db, customer_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get customer by ID."""
    try:
        return get_customer(db, customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{customer_id}", response_model=CustomerOut)
async def update_customer_endpoint(
    customer_id: int,
    customer_update: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update customer information."""
    try:
        return update_customer(db, customer_id, customer_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{customer_id}")
async def delete_customer_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete customer."""
    try:
        delete_customer(db, customer_id)
        return {"message": "Customer deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
