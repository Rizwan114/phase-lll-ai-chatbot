# Authentication Implementation Patterns

This document describes the authentication patterns and practices implemented in the Todo Application backend.

## Architecture Overview

The authentication system is built using JWT (JSON Web Tokens) with the following components:

- **JWT Configuration**: Located in `src/config/jwt_config.py`
- **Authentication Handler**: Located in `src/auth/auth_handler.py`
- **Authentication Middleware**: Located in `src/auth/middleware.py`
- **Error Handling**: Located in `src/utils/error_handlers.py` and `src/handlers/auth_errors.py`
- **Utility Functions**: Located in `src/utils/jwt_utils.py`

## JWT Token Structure

The JWT tokens contain the following claims:

- `sub`: Subject (user ID)
- `user_id`: User identifier (same as sub, but explicitly included)
- `exp`: Expiration timestamp
- `iat`: Issue timestamp

## Token Expiration and Security

- Access tokens expire after 30 minutes by default (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Tokens are validated using a shared secret key
- Tokens are stateless (no server-side storage required)
- User identity is extracted from the token payload

## Authentication Flow

1. **Token Creation**: When a user authenticates, a JWT token is created with the user's ID
2. **Token Attachment**: The client includes the token in the `Authorization: Bearer <token>` header
3. **Token Validation**: The server validates the token signature and expiration
4. **User Extraction**: The server extracts the user ID from the token
5. **Authorization**: The server ensures the extracted user ID matches the user ID in the route

## Security Measures

- **Signature Validation**: All tokens are validated against the shared secret key
- **Expiration Checking**: Expired tokens are rejected
- **User Isolation**: All database queries are scoped by the user ID in the token
- **Error Handling**: Authentication failures return standard HTTP 401/403 responses

## API Endpoint Protection

All API endpoints follow this pattern:

```python
@router.get("/{user_id}/tasks", response_model=TaskListResponse)
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )
```

## Configuration

Authentication behavior is controlled through environment variables:

- `SECRET_KEY`: JWT signing secret (required)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration in minutes (default: 30)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration in days (default: 7)

## Error Responses

Authentication errors return standardized JSON responses:

- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: Valid token but insufficient permissions

## Environment Variables

The system expects the following environment variables to be set:

```bash
# JWT Configuration
SECRET_KEY="your-super-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_ISSUER="todo-app"
JWT_AUDIENCE="todo-users"
```

## Testing

Authentication can be tested by:

1. Creating a valid JWT token
2. Making requests with the `Authorization: Bearer <token>` header
3. Verifying that unauthorized requests return 401/403
4. Verifying that expired tokens are rejected
5. Verifying that users can only access their own data