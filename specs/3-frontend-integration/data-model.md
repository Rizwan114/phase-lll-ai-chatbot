# Data Model: Frontend & Integration for Todo Full-Stack Web Application

## User Session Model

### AuthState
**Entity**: AuthState
**Description**: Represents the current authentication state of the application

**Fields**:
- `isAuthenticated` (boolean): Whether the user is currently authenticated
- `user` (User | null): User information when authenticated
- `token` (string | null): JWT token for authenticated requests
- `isLoading` (boolean): Whether auth state is being resolved
- `error` (string | null): Error message if authentication failed

**Validation Rules**:
- `isAuthenticated` must be consistent with presence of `token` and `user`
- `token` must be valid JWT format when present
- `isLoading` must be false when `error` is present

**State Transitions**:
- Initial → Loading (during app startup)
- Loading → Authenticated (with valid token)
- Loading → Unauthenticated (no token or invalid token)
- Authenticated → Unauthenticated (logout or token expiration)

## Task Model

### TaskFrontend
**Entity**: TaskFrontend
**Description**: Frontend representation of a task matching backend schema

**Fields**:
- `id` (number): Unique identifier for the task
- `title` (string): Task title (1-255 characters)
- `description` (string | null): Task description (0-1000 characters)
- `completed` (boolean): Whether the task is completed
- `user_id` (string): Associated user ID
- `created_at` (string): Creation timestamp (ISO 8601)
- `updated_at` (string): Last update timestamp (ISO 8601)

**Validation Rules**:
- `title` must be between 1 and 255 characters
- `description` can be null or between 0 and 1000 characters
- `completed` must be boolean type
- `user_id` must match authenticated user ID

**State Transitions**:
- New → Pending (when being created)
- Pending → Saved (after successful API call)
- Saved → Updating (when being modified)
- Updating → Saved (after successful update)
- Saved → Deleting (when being deleted)
- Deleting → Removed (after successful deletion)

## Loading State Model

### LoadingState
**Entity**: LoadingState
**Description**: Represents the loading state of various UI components

**Fields**:
- `isLoading` (boolean): Whether component is in loading state
- `progress` (number | null): Progress percentage if applicable (0-100)
- `message` (string | null): Optional message describing the loading process

**Validation Rules**:
- `progress` must be between 0 and 100 when present
- `message` should be user-friendly and localized

**State Transitions**:
- Idle → Loading (when action initiated)
- Loading → Success/Idle (when action completes)
- Loading → Error (when action fails)

## Error State Model

### ErrorState
**Entity**: ErrorState
**Description**: Represents the error state of various UI components

**Fields**:
- `hasError` (boolean): Whether an error has occurred
- `errorType` (string): Category of error (network, validation, auth, etc.)
- `message` (string): User-friendly error message
- `details` (string | null): Additional technical details for debugging
- `canRetry` (boolean): Whether the action can be retried

**Validation Rules**:
- `message` must be user-friendly and not expose sensitive information
- `errorType` must be one of predefined categories
- `hasError` must be false when no error exists

**State Transitions**:
- Idle → Error (when action fails)
- Error → Retry (when user retries action)
- Error → Idle (when error is resolved)

## API Request Model

### ApiRequest
**Entity**: ApiRequest
**Description**: Structure of API requests made from frontend

**Fields**:
- `url` (string): Target API endpoint
- `method` (string): HTTP method (GET, POST, PUT, DELETE, PATCH)
- `headers` (Record<string, string>): Request headers including Authorization
- `body` (any | null): Request payload for POST/PUT/PATCH requests
- `timestamp` (number): When request was made

**Validation Rules**:
- `method` must be a valid HTTP method
- `headers` must include Authorization when authenticated
- `body` must be properly serialized JSON when present

## API Response Model

### ApiResponse
**Entity**: ApiResponse
**Description**: Structure of API responses received by frontend

**Fields**:
- `success` (boolean): Whether request was successful
- `data` (any | null): Response data when successful
- `error` (string | null): Error message when unsuccessful
- `status` (number): HTTP status code
- `timestamp` (number): When response was received

**Validation Rules**:
- `success` must align with `status` code and presence of `data`/`error`
- `status` must be valid HTTP status code
- `error` must not expose sensitive server information

## Navigation State Model

### NavigationState
**Entity**: NavigationState
**Description**: Represents the current navigation state of the application

**Fields**:
- `currentPath` (string): Current URL path
- `previousPath` (string | null): Previous URL path
- `isLoading` (boolean): Whether navigation is in progress
- `isProtected` (boolean): Whether current route requires authentication

**Validation Rules**:
- `currentPath` must be valid relative path
- `isProtected` must be determined from route configuration

**State Transitions**:
- Path A → Loading → Path B (during navigation)
- Loading → Path B (navigation successful)
- Loading → Path A (navigation failed)