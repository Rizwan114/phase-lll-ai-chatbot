# Research: JWT Authentication Architecture for Next.js + FastAPI Integration

## R0.1: JWT Payload Fields for Backend

**Decision**: JWT tokens will include the following standard claims:
- `sub` (subject): user identifier (UUID or string)
- `exp` (expiration): Unix timestamp for token expiration
- `iat` (issued at): Unix timestamp for token creation
- `user_id`: Custom claim for user identification (matches route parameter)

**Rationale**: The `user_id` claim provides a clear, standardized way for the backend to identify the authenticated user and compare it with the user_id in route parameters. Standard JWT claims ensure compatibility with common libraries.

**Alternatives considered**:
- Using `sub` claim directly vs. custom `user_id` claim: Decided to use both for maximum compatibility
- Including user roles/permissions in token: Out of scope for this feature (no role-based permissions)
- Adding additional user profile data: Not needed for basic authentication

## R0.2: Token Expiration Duration and Validation Rules

**Decision**: Use 24-hour expiration for access tokens with no refresh token mechanism for this implementation.

**Rationale**: 24 hours provides a good balance between security (short-lived tokens reduce exposure window) and user experience (users won't need to re-authenticate frequently). Since this is a simple todo application, complex refresh token logic is not needed.

**Alternatives considered**:
- 1-hour tokens: More secure but worse UX
- 7-day tokens: Better UX but less secure
- Refresh token implementation: Adds complexity beyond current requirements

**Validation rules**:
- Token must not be expired (exp > current time)
- Token signature must match shared secret
- Token must include valid user_id claim

## R0.3: Strategy for Matching JWT User Identity with Route user_id

**Decision**: Implement middleware that extracts `user_id` from JWT claims and compares it with the `user_id` path parameter in routes.

**Rationale**: This enforces proper user isolation by ensuring the authenticated user can only access resources belonging to their account. The comparison happens at the authentication middleware level for all protected routes.

**Implementation approach**:
- JWT contains `user_id` claim identifying the authenticated user
- Route parameter contains `user_id` specifying the requested resource owner
- Middleware compares these values and returns 403 Forbidden if they don't match
- Special consideration for admin or superuser access (not implemented in this scope)

**Alternatives considered**:
- Database lookup approach: Against spec requirement for stateless validation
- Session-based approach: Violates statelessness requirement
- Different user identification method: JWT claims are the standard approach

## R0.4: Better Auth Integration Patterns

**Decision**: Use Better Auth's built-in JWT generation with custom configuration to include required claims.

**Rationale**: Better Auth provides secure, well-tested JWT implementation that reduces security risks compared to custom implementation. It also handles token refresh and other complexities.

**Implementation approach**:
- Configure Better Auth to include custom `user_id` claim in JWT
- Use Better Auth's client-side functions for token management
- Implement API client wrapper that automatically attaches Authorization header

## R0.5: FastAPI JWT Middleware Best Practices

**Decision**: Create a FastAPI dependency using `HTTPBearer` for token extraction and `jose.JWTError` for validation.

**Rationale**: This follows FastAPI best practices for authentication dependencies and integrates cleanly with existing route handlers. The dependency approach allows easy reuse across endpoints.

**Implementation approach**:
- Create `get_current_user` dependency that validates JWT
- Use `Depends()` to inject authenticated user into route handlers
- Return 401 Unauthorized for invalid/missing tokens
- Handle specific JWT errors appropriately

## Summary

All "known unknowns" from the implementation plan have been researched and resolved:

1. **JWT payload fields**: Will include standard claims plus `user_id` custom claim
2. **Token expiration**: 24-hour tokens with no refresh mechanism
3. **User identity matching**: Compare JWT `user_id` claim with route `user_id` parameter
4. **Security measures**: Stateless validation with shared secret
5. **Integration approach**: Better Auth for frontend, FastAPI dependency for backend