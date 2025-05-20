from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.address import Address
from schemas.address import AddressCreate, AddressOut
from utils.auth_dependency import get_current_user, get_db
from crud.address import create_address, get_address, update_address, delete_address
from models.user import User

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.post("/", response_model=AddressOut, status_code=201)
async def create_address_endpoint(
    address_in: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new address."""
    try:
        return create_address(db, address_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{address_id}", response_model=AddressOut)
async def get_address_endpoint(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get address by ID."""
    try:
        return get_address(db, address_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{address_id}", response_model=AddressOut)
async def update_address_endpoint(
    address_id: int,
    address_update: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update address information."""
    try:
        return update_address(db, address_id, address_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{address_id}")
async def delete_address_endpoint(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete address."""
    try:
        delete_address(db, address_id)
        return {"message": "Address deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
