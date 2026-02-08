# MCP Tool Contracts

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-08

## Overview

These 5 MCP tools are the ONLY mutation boundary in the system.
The AI agent MUST only use these tools. Each tool enforces user
ownership, validates input, and returns structured output.

All tools receive `user_id` as a required parameter to enforce
multi-user isolation.

---

## add_task

**Description**: Create a new task for the user.

**Input Schema**:
```json
{
  "user_id": "string (required)",
  "title": "string (required, 1-255 chars)",
  "description": "string (optional, 0-1000 chars)"
}
```

**Output (success)**:
```json
{
  "status": "success",
  "task": {
    "id": 1,
    "title": "buy groceries",
    "description": null,
    "completed": false,
    "created_at": "2026-02-08T12:00:00"
  }
}
```

**Output (error)**:
```json
{
  "status": "error",
  "message": "Title is required"
}
```

**Service mapping**: `TaskService.create_task()`

---

## list_tasks

**Description**: List all tasks for the user.

**Input Schema**:
```json
{
  "user_id": "string (required)"
}
```

**Output (success)**:
```json
{
  "status": "success",
  "tasks": [
    {
      "id": 1,
      "title": "buy groceries",
      "description": null,
      "completed": false,
      "created_at": "2026-02-08T12:00:00"
    }
  ],
  "count": 1
}
```

**Output (empty)**:
```json
{
  "status": "success",
  "tasks": [],
  "count": 0
}
```

**Service mapping**: `TaskService.get_tasks_by_user()`

---

## complete_task

**Description**: Mark a task as completed (toggle).

**Input Schema**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)"
}
```

**Output (success)**:
```json
{
  "status": "success",
  "task": {
    "id": 1,
    "title": "buy groceries",
    "completed": true,
    "updated_at": "2026-02-08T12:30:00"
  }
}
```

**Output (not found)**:
```json
{
  "status": "error",
  "message": "Task with ID 999 not found for this user"
}
```

**Service mapping**: `TaskService.toggle_task_completion()`

---

## update_task

**Description**: Update a task's title or description.

**Input Schema**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)",
  "title": "string (optional, 1-255 chars)",
  "description": "string (optional, 0-1000 chars)"
}
```

**Output (success)**:
```json
{
  "status": "success",
  "task": {
    "id": 1,
    "title": "buy groceries and snacks",
    "description": "From the store on Main St",
    "completed": false,
    "updated_at": "2026-02-08T12:30:00"
  }
}
```

**Output (not found)**:
```json
{
  "status": "error",
  "message": "Task with ID 999 not found for this user"
}
```

**Output (no fields)**:
```json
{
  "status": "error",
  "message": "At least one field (title or description) must be provided"
}
```

**Service mapping**: `TaskService.update_task()`

---

## delete_task

**Description**: Delete a task permanently.

**Input Schema**:
```json
{
  "user_id": "string (required)",
  "task_id": "integer (required)"
}
```

**Output (success)**:
```json
{
  "status": "success",
  "message": "Task 1 deleted successfully"
}
```

**Output (not found)**:
```json
{
  "status": "error",
  "message": "Task with ID 999 not found for this user"
}
```

**Service mapping**: `TaskService.delete_task()`

---

## Common Contracts

### User Ownership
Every tool MUST receive `user_id` and MUST scope all database queries
to that user. A tool MUST NOT return or modify tasks belonging to
other users.

### Error Format
All errors MUST use the structure:
```json
{ "status": "error", "message": "Human-readable error description" }
```

### Input Validation
- All required fields MUST be present
- String lengths MUST be within defined bounds
- task_id MUST be a positive integer
- user_id MUST be a non-empty string
