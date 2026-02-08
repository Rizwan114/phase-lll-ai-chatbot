# Data Model: Authentication & Security Layer for Todo Full-Stack Web Application

## JWT Token Structure

### JWT Claims Model
**Entity**: JWTClaims
**Description**: The structure of claims contained within JWT tokens

**Fields**:
- `sub` (string): Subject identifier - unique user ID
- `exp` (integer): Expiration time (Unix timestamp)
- `iat` (integer): Issued at time (Unix timestamp)
- `user_id` (string): User identifier that matches route parameter

**Validation Rules**:
- `sub` must be a valid UUID or alphanumeric string
- `exp` must be greater than current time
- `iat` must be less than or equal to current time
- `user_id` must be a non-empty string

**State Transitions**:
- Active (when issued) → Expired (when exp < current time)

## User Identity Model

### Authenticated User
**Entity**: AuthenticatedUser
**Description**: Represents an authenticated user with their identity claims

**Fields**:
- `user_id` (string): Unique identifier for the user
- `is_authenticated` (boolean): Whether the user is currently authenticated
- `token_expiry` (datetime): When the current token expires

**Relationships**:
- Links to Task entities (one user to many tasks)
- Verifies ownership of tasks accessed via API

## Authorization Header Model

### AuthHeader
**Entity**: AuthorizationHeader
**Description**: Structure of the authorization header sent with API requests

**Fields**:
- `scheme` (string): Must be "Bearer"
- `token` (string): JWT token string

**Validation Rules**:
- Must follow format: "Bearer <token>"
- Token must be valid JWT format (3 parts separated by dots)
- Token must pass signature validation

## Error Response Model

### AuthErrorResponse
**Entity**: AuthErrorResponse
**Description**: Standardized error responses for authentication failures

**Fields**:
- `error` (string): Error code (e.g., "UNAUTHORIZED", "TOKEN_EXPIRED", "INVALID_TOKEN")
- `message` (string): Human-readable error message
- `timestamp` (datetime): When the error occurred

**HTTP Status Codes**:
- 401: UNAUTHORIZED (invalid/missing token)
- 403: FORBIDDEN (valid token but insufficient privileges)

## Session State Model

### ClientSession
**Entity**: ClientSession
**Description**: Frontend representation of authentication state

**Fields**:
- `is_logged_in` (boolean): Whether user is currently logged in
- `user_id` (string): Current user's identifier
- `access_token` (string): Current JWT access token
- `expires_at` (datetime): When current token expires

**State Transitions**:
- Anonymous → Logged In (after successful authentication)
- Logged In → Anonymous (after logout or token expiration)

## Backend Validation Model

### TokenValidationResult
**Entity**: TokenValidationResult
**Description**: Result of JWT validation process

**Fields**:
- `is_valid` (boolean): Whether token is valid
- `user_id` (string): Extracted user ID from token (if valid)
- `error_message` (string): Reason for invalidation (if invalid)
- `expires_at` (datetime): Token expiration time (if valid)

**Validation Process**:
- Signature verification against shared secret
- Expiration check
- User identity extraction