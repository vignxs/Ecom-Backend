from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from sqlalchemy import Enum as SqlEnum
from .order_status import OrderStatus

from models.customer import Customer
from models.invoice import Invoice
from models.address import Address
from models.order_product import OrderProduct

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(20), unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50))
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    customer = relationship("Customer", back_populates="orders")
    shipping_address = relationship("Address", uselist=False, back_populates="order")
    order_products = relationship("OrderProduct", back_populates="order")
    invoice = relationship("Invoice", uselist=False, back_populates="order")
    user = relationship("User", back_populates="orders")

