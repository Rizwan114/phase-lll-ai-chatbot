"""
Authentication-related data models for the Todo Application
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    """
    JWT Token response model
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class TokenData(BaseModel):
    """
    JWT Token data model
    Contains the information extracted from a JWT token
    """
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None


class UserLoginRequest(BaseModel):
    """
    Request model for user login
    """
    username: str
    password: str


class UserRegisterRequest(BaseModel):
    """
    Request model for user registration
    """
    username: str
    email: str
    password: str


class AuthResponse(BaseModel):
    """
    Response model for authentication operations
    """
    success: bool
    message: str
    user_id: Optional[str] = None
    token: Optional[Token] = None