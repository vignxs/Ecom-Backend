from typing import List, Optional
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product_data: ProductCreate) -> Product:
    """Create a new product."""
    try:
        # Check if permalink exists
        existing = db.query(Product).filter(Product.permalink == product_data.permalink).first()
        if existing:
            raise ValueError("Permalink already exists")
        
        product = Product(**product_data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create product: {str(e)}")

def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    """Get list of products with pagination."""
    try:
        return db.query(Product).offset(skip).limit(limit).all()
    except Exception as e:
        raise ValueError(f"Failed to fetch products: {str(e)}")

def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Get a single product by ID."""
    try:
        return db.query(Product).filter(Product.id == product_id).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch product: {str(e)}")

def update_product(db: Session, product_id: int, update_data: ProductUpdate) -> Product:
    """Update an existing product."""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update product: {str(e)}")

def delete_product(db: Session, product_id: int) -> None:
    """Delete a product."""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product not found")
        
        db.delete(product)
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete product: {str(e)}")
