from fastapi import APIRouter
from schemas.product import ProductCreate
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from utils.auth_dependency import get_current_user, get_db
from models.user import User
from models.product import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def list_products():
    return {"products": ["Product A", "Product B"]}


@router.post("/products/", status_code=201)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # if you want to limit access
):
    # Check if permalink is unique
    existing = db.query(Product).filter(Product.permalink == product_in.permalink).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permalink already exists")

    product = Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
