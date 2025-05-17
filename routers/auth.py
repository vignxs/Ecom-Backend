import random
from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from schemas.user import *
from utils.auth_dependency import get_current_user, get_db
from utils.email_service import send_email
from utils.jwt_handler import create_access_token, create_refresh_token, verify_token

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signin", response_model=Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token (1 minute expiry)
    access_token = create_access_token(
        data={"sub": user.email}
    )

    # Create refresh token (30 minutes expiry)
    refresh_token = create_refresh_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    code = str(random.randint(100000, 999999))
    user.reset_code = code
    db.commit()

    background_tasks.add_task(send_email, user.email, "Password Reset Code", f"Use this code to reset your password: {code}")
    return {"message": "Reset code sent to your email"}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or user.reset_code != request.code:
        raise HTTPException(status_code=400, detail="Invalid code or email")

    user.hashed_password = pwd_context.hash(request.new_password)
    user.reset_code = None
    db.commit()
    return {"message": "Password reset successful"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(request: RefreshTokenRequest):
    # Verify the refresh token
    payload = verify_token(request.refresh_token, token_type="refresh")

    # Extract user email from the token
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a new access token
    access_token = create_access_token(data={"sub": email})

    # Create a new refresh token (optional, you can also keep the same refresh token)
    refresh_token = create_refresh_token(data={"sub": email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
