from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from sqlalchemy import Enum as SqlEnum
from enum import Enum

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_country_code = Column(String(10))
    phone_number = Column(String(20))

    orders = relationship("Order", back_populates="customer")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    customer_name = Column(String, nullable=False)
    issued_date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # Linking with order
    order = relationship("Order", back_populates="invoice")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    building = Column(String(100))
    apartment_no = Column(String(50))
    house_no = Column(String(50))
    street = Column(String(100))
    city = Column(String(50))
    country = Column(String(50))    

    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="shipping_address")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)
    name = Column(String(100))
    price = Column(Float, nullable=False)

    order_products = relationship("OrderProduct", back_populates="product")

class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    discount = Column(Float, default=0.0)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")

class OrderStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

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

