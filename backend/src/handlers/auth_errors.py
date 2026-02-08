"""
Authentication Error Handlers for the Todo Application
Provides standardized error responses for authentication-related failures
"""
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def handle_auth_exception(exc: Exception, user_id: str = None, endpoint: str = None) -> JSONResponse:
    """
    Handle authentication-related exceptions and return standardized error responses

    Args:
        exc: The exception that occurred
        user_id: Optional user ID for logging context
        endpoint: Optional endpoint for logging context

    Returns:
        JSONResponse with standardized error format
    """
    # Log the error with context
    log_details = f"Authentication error in {endpoint}" if endpoint else "Authentication error"
    if user_id:
        log_details += f" for user {user_id}"

    logger.error(f"{log_details}: {str(exc)}", extra={
        "user_id": user_id,
        "endpoint": endpoint,
        "exception_type": type(exc).__name__
    })

    # Return appropriate error response based on exception type
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "AUTHENTICATION_FAILED",
                "message": exc.detail,
                "timestamp": _get_timestamp()
            }
        )

    # For other exceptions, return a generic authentication error
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "AUTHENTICATION_FAILED",
            "message": "Authentication failed due to an unexpected error",
            "timestamp": _get_timestamp()
        }
    )


def unauthorized_error_response(message: str = "Unauthorized: Invalid or missing credentials") -> JSONResponse:
    """
    Create a standardized unauthorized error response

    Args:
        message: Error message to include in the response

    Returns:
        JSONResponse with 401 status code and standardized format
    """
    logger.warning(f"Unauthorized access attempt: {message}")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "UNAUTHORIZED",
            "message": message,
            "timestamp": _get_timestamp()
        }
    )


def forbidden_error_response(message: str = "Forbidden: Insufficient permissions") -> JSONResponse:
    """
    Create a standardized forbidden error response

    Args:
        message: Error message to include in the response

    Returns:
        JSONResponse with 403 status code and standardized format
    """
    logger.warning(f"Forbidden access attempt: {message}")

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "FORBIDDEN",
            "message": message,
            "timestamp": _get_timestamp()
        }
    )


def token_expired_error() -> JSONResponse:
    """
    Create a standardized token expired error response

    Returns:
        JSONResponse with 401 status code for expired token
    """
    logger.info("Token expired error triggered")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "TOKEN_EXPIRED",
            "message": "Authentication token has expired",
            "timestamp": _get_timestamp()
        }
    )


def invalid_token_error() -> JSONResponse:
    """
    Create a standardized invalid token error response

    Returns:
        JSONResponse with 401 status code for invalid token
    """
    logger.warning("Invalid token error triggered")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "INVALID_TOKEN",
            "message": "Invalid authentication token",
            "timestamp": _get_timestamp()
        }
    )


def insufficient_scope_error(required_scopes: list = None) -> JSONResponse:
    """
    Create a standardized insufficient scope error response

    Args:
        required_scopes: List of scopes that were required

    Returns:
        JSONResponse with 403 status code for insufficient scope
    """
    message = "Insufficient permissions to access this resource"
    if required_scopes:
        message += f". Required scopes: {', '.join(required_scopes)}"

    logger.warning(f"Insufficient scope error: {message}")

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "INSUFFICIENT_SCOPE",
            "message": message,
            "timestamp": _get_timestamp()
        }
    )


def user_not_found_error(user_identifier: str = None) -> JSONResponse:
    """
    Create a standardized user not found error response

    Args:
        user_identifier: Optional identifier of the user that wasn't found

    Returns:
        JSONResponse with 401 status code for user not found
    """
    message = "User not found or no longer exists"
    if user_identifier:
        message = f"User '{user_identifier}' not found or no longer exists"

    logger.info(f"User not found error: {message}")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "USER_NOT_FOUND",
            "message": message,
            "timestamp": _get_timestamp()
        }
    )


def _get_timestamp() -> str:
    """
    Get current timestamp in ISO format

    Returns:
        Current timestamp as ISO string
    """
    from datetime import datetime
    return datetime.utcnow().isoformat() + "Z"


# Exception handlers for FastAPI
def auth_exception_handler(request, exc):
    """
    FastAPI exception handler for authentication errors
    """
    return handle_auth_exception(exc, endpoint=str(request.url))


def unauthorized_exception_handler(request, exc):
    """
    FastAPI exception handler for unauthorized access
    """
    return unauthorized_error_response(str(exc.detail) if hasattr(exc, 'detail') else "Unauthorized access")


def forbidden_exception_handler(request, exc):
    """
    FastAPI exception handler for forbidden access
    """
    return forbidden_error_response(str(exc.detail) if hasattr(exc, 'detail') else "Forbidden access")