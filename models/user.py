from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    otp = Column(String, nullable=True)
    reset_code = Column(String, nullable=True)

    # Use string reference to avoid circular imports
    orders = relationship("Order", back_populates="user", lazy="dynamic")
