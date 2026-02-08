# API Contracts: Frontend & Integration for Todo Full-Stack Web Application

## Authentication Endpoints

### POST /api/auth/login
Authenticate user and return JWT token

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response (200)**:
```json
{
  "user": {
    "id": "user-uuid",
    "user_id": "user-uuid",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
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

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "username": "john_doe"
}
```

**Success Response (201)**:
```json
{
  "user": {
    "id": "user-uuid",
    "user_id": "user-uuid",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

**Error Response (400)**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Email is already in use"
}
```

### POST /api/auth/logout
Logout user and invalidate session

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Success Response (204)**: No content

## Task Management Endpoints

### GET /api/{user_id}/tasks
Get all tasks for authenticated user

**Request Headers**:
```
Authorization: Bearer {access_token}
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
      "user_id": "user-uuid",
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

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
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
  "user_id": "user-uuid",
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

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Success Response (200)**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Sample description",
  "completed": false,
  "user_id": "user-uuid",
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

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Request Body**:
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
  "user_id": "user-uuid",
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

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Success Response (204)**: No content

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 404: Task not found

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle completion status of a specific task for authenticated user

**Request Headers**:
```
Authorization: Bearer {access_token}
```

**Success Response (200)**:
```json
{
  "id": 1,
  "title": "Sample task",
  "description": "Sample description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

**Error Responses**:
- 401: Invalid or missing token
- 403: Token user_id doesn't match route user_id
- 404: Task not found

## Frontend Component Contracts

### Authentication Components

#### LoginForm Component
- Props: `onLogin: (credentials) => Promise<AuthResult>`
- Events: `submit`, `error`
- State: `loading`, `error`

#### SignupForm Component
- Props: `onSignup: (userData) => Promise<AuthResult>`
- Events: `submit`, `error`
- State: `loading`, `error`

### Task Components

#### TaskList Component
- Props: `tasks: Task[], onTaskUpdate: (task) => void, onTaskDelete: (taskId) => void`
- Events: `taskCreated`, `taskUpdated`, `taskDeleted`
- State: `loading`, `empty`, `error`

#### TaskItem Component
- Props: `task: Task, onUpdate: (task) => void, onDelete: (taskId) => void`
- Events: `toggleComplete`, `edit`, `delete`
- State: `editing`, `deleting`

#### TaskForm Component
- Props: `onSubmit: (taskData) => void, initialData?: Task`
- Events: `submit`, `cancel`
- State: `loading`, `error`