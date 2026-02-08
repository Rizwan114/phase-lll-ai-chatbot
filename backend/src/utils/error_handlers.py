"""
Error handlers and utilities for the Todo Application
Provides centralized error handling for authentication and other operations
"""
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """
    Base exception class for authentication-related errors
    """
    def __init__(self, message: str, error_code: str = "AUTH_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class TokenValidationError(AuthError):
    """
    Exception raised when JWT token validation fails
    """
    def __init__(self, message: str = "Token validation failed"):
        super().__init__(message, "TOKEN_VALIDATION_ERROR")


class UserNotFoundError(AuthError):
    """
    Exception raised when a user is not found in the system
    """
    def __init__(self, message: str = "User not found"):
        super().__init__(message, "USER_NOT_FOUND")


class InsufficientPermissionsError(AuthError):
    """
    Exception raised when a user doesn't have sufficient permissions
    """
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, "INSUFFICIENT_PERMISSIONS")


def handle_auth_error(request: Request, exc: AuthError) -> JSONResponse:
    """
    Handle authentication-related errors

    Args:
        request: The incoming request
        exc: The authentication error

    Returns:
        JSONResponse with error details
    """
    logger.warning(f"Authentication error: {exc.error_code} - {exc.message}")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "detail": exc.message
        }
    )


def handle_permission_error(request: Request, exc: InsufficientPermissionsError) -> JSONResponse:
    """
    Handle permission-related errors

    Args:
        request: The incoming request
        exc: The permission error

    Returns:
        JSONResponse with error details
    """
    logger.warning(f"Permission error: {exc.error_code} - {exc.message}")

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "detail": exc.message
        }
    )


def handle_unauthorized_error():
    """
    Raise a standardized unauthorized error for authentication failures
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized: Invalid or missing authentication credentials"
    )


def handle_forbidden_error(detail: str = "Forbidden: Insufficient permissions"):
    """
    Raise a standardized forbidden error for authorization failures

    Args:
        detail: Error message to include in the response
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )


def log_auth_error(error_type: str, error_message: str, user_id: str = None, ip_address: str = None):
    """
    Log authentication-related errors with context

    Args:
        error_type: Type of authentication error
        error_message: Details about the error
        user_id: Optional user ID involved in the error
        ip_address: Optional IP address of the request
    """
    extra_context = {}
    if user_id:
        extra_context["user_id"] = user_id
    if ip_address:
        extra_context["ip_address"] = ip_address

    logger.error(f"Authentication {error_type}: {error_message}", extra=extra_context)


def validate_user_access(requested_user_id: str, authenticated_user_id: str) -> bool:
    """
    Validate that the requested user ID matches the authenticated user ID

    Args:
        requested_user_id: User ID from the request/route
        authenticated_user_id: User ID from the authentication token

    Returns:
        bool: True if IDs match, raises HTTPException if not
    """
    if requested_user_id != authenticated_user_id:
        handle_forbidden_error(f"Access denied: Cannot access resources for user {requested_user_id}")
        return False
    return True