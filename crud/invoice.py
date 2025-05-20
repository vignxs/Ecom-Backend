from typing import Optional
from sqlalchemy.orm import Session
from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceUpdate

def create_invoice(db: Session, invoice_data: InvoiceCreate) -> Invoice:
    """Create a new invoice."""
    try:
        invoice = Invoice(**invoice_data.dict())
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create invoice: {str(e)}")

def get_invoice(db: Session, invoice_id: int) -> Optional[Invoice]:
    """Get an invoice by ID."""
    try:
        return db.query(Invoice).filter(Invoice.id == invoice_id).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch invoice: {str(e)}")

def get_invoice_by_order(db: Session, order_id: int) -> Optional[Invoice]:
    """Get invoice by order ID."""
    try:
        return db.query(Invoice).filter(Invoice.order_id == order_id).first()
    except Exception as e:
        raise ValueError(f"Failed to fetch invoice: {str(e)}")

def update_invoice(db: Session, invoice_id: int, update_data: InvoiceUpdate) -> Invoice:
    """Update an existing invoice."""
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise ValueError("Invoice not found")
        
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(invoice, key, value)
        
        db.commit()
        db.refresh(invoice)
        return invoice
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to update invoice: {str(e)}")

def delete_invoice(db: Session, invoice_id: int) -> None:
    """Delete an invoice."""
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise ValueError("Invoice not found")
        
        db.delete(invoice)
        db.commit()
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to delete invoice: {str(e)}")
