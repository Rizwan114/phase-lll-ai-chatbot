"""
JWT Utility Functions for the Todo Application
Provides helper functions for JWT operations including validation, encoding, and decoding
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError
import os
from ..config.jwt_config import SECRET_KEY, ALGORITHM


def encode_jwt(payload: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Encode a JWT token with the given payload

    Args:
        payload: Dictionary containing the claims to include in the token
        expires_delta: Optional timedelta for token expiration

    Returns:
        Encoded JWT token string
    """
    to_encode = payload.copy()

    # Set expiration if provided
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiration: 30 minutes
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    # Encode the token
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def decode_jwt(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token and return its payload

    Args:
        token: JWT token string to decode

    Returns:
        Dictionary containing the token payload, or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Log the error in a real application
        return None


def validate_jwt_token(token: str) -> bool:
    """
    Validate a JWT token without returning its payload

    Args:
        token: JWT token string to validate

    Returns:
        Boolean indicating whether the token is valid
    """
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract the user ID from a JWT token

    Args:
        token: JWT token string

    Returns:
        User ID string if found and token is valid, None otherwise
    """
    payload = decode_jwt(token)
    if payload:
        # Assuming 'sub' (subject) or 'user_id' field contains the user ID
        return payload.get('sub') or payload.get('user_id')
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired

    Args:
        token: JWT token string

    Returns:
        Boolean indicating whether the token is expired
    """
    payload = decode_jwt(token)
    if not payload:
        return True  # If we can't decode it, treat as expired

    exp_timestamp = payload.get('exp')
    if not exp_timestamp:
        return True  # If no expiration, treat as expired

    # Convert to datetime and check
    exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
    current_datetime = datetime.utcnow()

    return current_datetime > exp_datetime


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with the given data

    Args:
        data: Dictionary containing the claims to include in the token
        expires_delta: Optional timedelta for token expiration

    Returns:
        Encoded JWT access token string
    """
    return encode_jwt(data, expires_delta)


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a refresh token with the given data

    Args:
        data: Dictionary containing the claims to include in the token
        expires_delta: Optional timedelta for token expiration (defaults to 7 days)

    Returns:
        Encoded JWT refresh token string
    """
    if expires_delta is None:
        # Default refresh token expiration: 7 days
        expires_delta = timedelta(days=7)

    return encode_jwt(data, expires_delta)


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Generate a new access token from a refresh token

    Args:
        refresh_token: Valid refresh token string

    Returns:
        New access token string if refresh token is valid, None otherwise
    """
    if not validate_jwt_token(refresh_token):
        return None

    # Get the original data from the refresh token
    original_payload = decode_jwt(refresh_token)
    if not original_payload:
        return None

    # Remove expiration to create new token with current timestamp
    if 'exp' in original_payload:
        del original_payload['exp']

    # Create new access token with standard expiration (30 minutes)
    new_access_token = create_access_token(original_payload, timedelta(minutes=30))
    return new_access_token


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration datetime of a JWT token

    Args:
        token: JWT token string

    Returns:
        Expiration datetime if found, None otherwise
    """
    payload = decode_jwt(token)
    if not payload:
        return None

    exp_timestamp = payload.get('exp')
    if not exp_timestamp:
        return None

    return datetime.utcfromtimestamp(exp_timestamp)


def get_time_until_expiration(token: str) -> Optional[timedelta]:
    """
    Get the time remaining until a token expires

    Args:
        token: JWT token string

    Returns:
        Timedelta representing time until expiration, None if token invalid
    """
    exp_datetime = get_token_expiration(token)
    if not exp_datetime:
        return None

    current_datetime = datetime.utcnow()
    time_remaining = exp_datetime - current_datetime

    # Return None if already expired
    if time_remaining.total_seconds() <= 0:
        return None

    return time_remaining