# API Contract: Authentication Endpoints

## Authentication Endpoints (Frontend Integration)

### POST /api/auth/login
Authenticate user and return JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response (200)**:
```json
{
  "user_id": "user-uuid-string",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

**Error Response (401)**:
```json
{
  "error": "UNAUTHORIZED",
  "message": "Invalid credentials"
}
```

### POST /api/auth/signup
Register new user and return JWT token

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Success Response (201)**:
```json
{
  "user_id": "user-uuid-string",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

**Error Response (400)**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid input data"
}
```

## Protected Task Endpoints (Updated with Authentication)

### GET /api/{user_id}/tasks
Get all tasks for authenticated user

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200)**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Sample description",
      "completed": false,
      "user_id": "user-uuid-string",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 500: Server error

### POST /api/{user_id}/tasks
Create a new task for authenticated user

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request**:
```json
{
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

**Success Response (201)**:
```json
{
  "id": 1,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid-string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 422: Validation error

### GET /api/{user_id}/tasks/{id}
Get a specific task for authenticated user

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200)**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Sample description",
  "completed": false,
  "user_id": "user-uuid-string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 404: Task not found

### PUT /api/{user_id}/tasks/{id}
Update a specific task for authenticated user

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request**:
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": true
}
```

**Success Response (200)**:
```json
{
  "id": 1,
  "title": "Updated task",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid-string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 404: Task not found

### DELETE /api/{user_id}/tasks/{id}
Delete a specific task for authenticated user

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (204)**: No content

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 404: Task not found

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle completion status of a specific task for authenticated user

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200)**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Sample description",
  "completed": true,
  "user_id": "user-uuid-string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 404: Task not found