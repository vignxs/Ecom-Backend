from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

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
