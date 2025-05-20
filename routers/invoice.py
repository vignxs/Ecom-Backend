from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.invoice import Invoice
from schemas.invoice import InvoiceListOut
from utils.auth_dependency import get_current_user, get_db
from crud.invoice import create_invoice, get_invoice, update_invoice, delete_invoice
from models.user import User
from typing import List

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceListOut, status_code=201)
async def create_invoice_endpoint(
    invoice_in: InvoiceListOut,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new invoice."""
    try:
        return create_invoice(db, invoice_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[InvoiceListOut])
async def list_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List invoices with pagination."""
    try:
        return get_invoices(db, skip, limit)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{invoice_id}", response_model=InvoiceListOut)
async def get_invoice_endpoint(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get invoice by ID."""
    try:
        return get_invoice(db, invoice_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{invoice_id}", response_model=InvoiceListOut)
async def update_invoice_endpoint(
    invoice_id: int,
    invoice_update: InvoiceListOut,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update invoice information."""
    try:
        return update_invoice(db, invoice_id, invoice_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{invoice_id}")
async def delete_invoice_endpoint(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete invoice."""
    try:
        delete_invoice(db, invoice_id)
        return {"message": "Invoice deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
