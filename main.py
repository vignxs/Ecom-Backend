from contextlib import asynccontextmanager

from fastapi import FastAPI
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from database import Base, SessionLocal, engine
from models.user import User
from models.order import Order, OrderStatus
from routers import auth, order, customer, invoice, address, order_product, product, shipping

Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if existing_admin:
            print(f"Admin user already exists with email: {settings.ADMIN_EMAIL}")
            return

        # Create new admin user
        hashed_password = pwd_context.hash(settings.ADMIN_PASSWORD)
        admin = User(
            email=settings.ADMIN_EMAIL,
            name=settings.ADMIN_NAME,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        print(f"Admin user created successfully!")
        print(f"Email: {settings.ADMIN_EMAIL}")
        print(f"Name: {settings.ADMIN_NAME}")
        
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_admin_user()
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(order.router)
app.include_router(shipping.router)
app.include_router(customer.router)
app.include_router(invoice.router)
app.include_router(address.router)
app.include_router(order_product.router)
app.include_router(product.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)