from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from utils.auth_dependency import get_current_user, get_db
from crud.product import create_product, get_products, get_product, update_product, delete_product
from models.user import User

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    """List products with pagination."""
    try:
        return get_products(db, skip, limit)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=201)
async def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new product."""
    try:
        return create_product(db, product_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{product_id}")
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a single product by ID."""
    try:
        product = get_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}")
async def update_product(
    product_id: int,
    update_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing product."""
    try:
        return update_product(db, product_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a product."""
    try:
        delete_product(db, product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
