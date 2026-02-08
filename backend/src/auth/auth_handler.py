from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlmodel import Session
import os
from ..config.jwt_config import SECRET_KEY, ALGORITHM, get_access_token_expire_delta
from ..database.database import engine
from ..utils.jwt_utils import decode_jwt, get_user_id_from_token
from ..handlers.auth_errors import invalid_token_error, token_expired_error

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + get_access_token_expire_delta()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """
    Verify a JWT token and return the decoded data
    """
    try:
        # Use utility function to extract user ID
        user_id = get_user_id_from_token(token)

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        token_data = TokenData(user_id=user_id)
        return token_data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get the current user from the token
    """
    token_data = verify_token(credentials.credentials)
    return token_data.user_id