"""
JWT Middleware for the Todo Application
Provides reusable authentication and authorization dependencies for FastAPI endpoints
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .auth_handler import verify_token
from ..utils.jwt_utils import is_token_expired, validate_jwt_token
from ..utils.logger import log_info, log_error


# Initialize HTTP Bearer scheme
security = HTTPBearer()


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to extract current user ID from JWT token
    Validates the token and returns the user ID

    Args:
        credentials: HTTP Authorization credentials containing the JWT

    Returns:
        str: User ID extracted from the token

    Raises:
        HTTPException: If token is invalid or user ID cannot be extracted
    """
    # Validate token signature first
    if not validate_jwt_token(credentials.credentials):
        log_error("Invalid token signature", extra={"method": "get_current_user_from_token"})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    # Check if token is expired
    if is_token_expired(credentials.credentials):
        log_error("Token has expired", extra={"method": "get_current_user_from_token"})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    # Verify and extract user ID
    token_data = verify_token(credentials.credentials)

    log_info(f"Successfully authenticated user {token_data.user_id}", extra={
        "user_id": token_data.user_id,
        "method": "get_current_user_from_token"
    })

    return token_data.user_id


def require_authentication() -> str:
    """
    Dependency to require authentication for protected endpoints
    Returns the authenticated user's ID

    Returns:
        str: User ID of the authenticated user
    """
    return Depends(get_current_user_from_token)


def require_same_user(route_user_id: str, current_user_id: str = Depends(require_authentication())) -> bool:
    """
    Dependency to ensure the current user matches the user ID in the route
    Used to prevent users from accessing other users' data

    Args:
        route_user_id: User ID from the route path parameter
        current_user_id: User ID of the authenticated user (extracted from token)

    Returns:
        bool: True if user IDs match, raises HTTPException otherwise
    """
    if route_user_id != current_user_id:
        log_error(f"User {current_user_id} attempted to access resources for user {route_user_id}", extra={
            "requesting_user_id": current_user_id,
            "target_user_id": route_user_id,
            "method": "require_same_user"
        })

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    log_info(f"User {current_user_id} successfully authorized for user {route_user_id}", extra={
        "current_user_id": current_user_id,
        "route_user_id": route_user_id,
        "method": "require_same_user"
    })

    return True


def validate_token_signature_and_expiration(token: str) -> bool:
    """
    Validate JWT token signature and expiration

    Args:
        token: JWT token string to validate

    Returns:
        bool: True if token is valid and not expired, False otherwise
    """
    # Validate token signature
    is_valid = validate_jwt_token(token)
    if not is_valid:
        log_error("Token signature validation failed", extra={"method": "validate_token_signature_and_expiration"})
        return False

    # Check token expiration
    expired = is_token_expired(token)
    if expired:
        log_error("Token has expired", extra={"method": "validate_token_signature_and_expiration"})
        return False

    return True