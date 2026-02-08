"""
JWT Configuration for the Todo Application
"""
import os
from datetime import timedelta

# Get secret key from environment
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Token expiration settings
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# JWT settings
JWT_ISSUER = os.getenv("JWT_ISSUER", "todo-app")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "todo-users")


def get_access_token_expire_delta():
    """Get timedelta for access token expiration"""
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def get_refresh_token_expire_delta():
    """Get timedelta for refresh token expiration"""
    return timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)