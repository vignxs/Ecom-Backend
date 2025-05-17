import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt

from config import settings


def load_rsa_keys():
    if not os.path.exists(settings.KEYS_DIR):
        raise FileNotFoundError(
            "RSA keys not found. Please run 'python utils/generate_keys.py' to generate the keys."
        )

    private_key_path = os.path.join(settings.KEYS_DIR, "private_key.pem")
    public_key_path = os.path.join(settings.KEYS_DIR, "public_key.pem")

    if not os.path.exists(private_key_path) or not os.path.exists(public_key_path):
        raise FileNotFoundError(
            "RSA keys not found. Please run 'python utils/generate_keys.py' to generate the keys."
        )

    # Read the PEM files as strings instead of loading as cryptography objects
    with open(private_key_path, "r") as f:
        private_key = f.read()

    with open(public_key_path, "r") as f:
        public_key = f.read()

    return private_key, public_key

private_key, public_key = load_rsa_keys()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, public_key, algorithms=[settings.JWT_ALGORITHM])

        # Verify token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type} token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )