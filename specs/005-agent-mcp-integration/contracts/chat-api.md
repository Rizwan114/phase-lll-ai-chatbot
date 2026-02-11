# API Contract: Chat Endpoints

**Branch**: `005-agent-mcp-integration` | **Date**: 2026-02-11

## POST /api/{user_id}/chat

**Status**: Already implemented in `backend/src/api/chat_routes.py`

Send a user message and receive the agent's response.

### Request

**Path Parameters**:
- `user_id` (string, required): Authenticated user's ID

**Headers**:
- `Authorization: Bearer <jwt_token>` (required)
- `Content-Type: application/json`

**Body**:
```json
{
  "message": "Add buy groceries to my list",
  "conversation_id": "optional-uuid-string"
}
```

| Field           | Type   | Required | Constraints          |
| --------------- | ------ | -------- | -------------------- |
| message         | string | yes      | 1-10000 chars        |
| conversation_id | string | no       | UUID of existing conv|

### Response (200 OK)

```json
{
  "conversation_id": "a1b2c3d4-e5f6-...",
  "response": "I've added 'buy groceries' to your list!",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": "{\"user_id\": \"user123\", \"title\": \"buy groceries\"}",
      "output": null
    }
  ]
}
```

| Field           | Type              | Description                      |
| --------------- | ----------------- | -------------------------------- |
| conversation_id | string            | UUID of the conversation         |
| response        | string            | Agent's natural language reply   |
| tool_calls      | ToolCallInfo[]?   | MCP tools invoked (nullable)     |

### Error Responses

| Status | Condition                    | Body                                    |
| ------ | ---------------------------- | --------------------------------------- |
| 401    | Missing/invalid/expired JWT  | `{"detail": "Invalid authentication token"}` |
| 403    | user_id mismatch with JWT    | `{"detail": "Forbidden"}`               |
| 404    | conversation_id not found    | `{"detail": "Conversation not found"}`  |
| 422    | Validation error (empty msg) | `{"detail": [validation errors]}`       |
| 500    | Agent/tool failure           | `{"detail": "Internal server error"}`   |

---

## GET /api/{user_id}/chat/history

**Status**: NEW — must be implemented

Load existing conversation history for the chat page.

### Request

**Path Parameters**:
- `user_id` (string, required): Authenticated user's ID

**Headers**:
- `Authorization: Bearer <jwt_token>` (required)

### Response (200 OK)

```json
{
  "conversation_id": "a1b2c3d4-e5f6-...",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Add buy groceries",
      "created_at": "2026-02-11T10:00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I've added 'buy groceries' to your list!",
      "created_at": "2026-02-11T10:00:02"
    }
  ]
}
```

| Field           | Type            | Description                       |
| --------------- | --------------- | --------------------------------- |
| conversation_id | string?         | UUID (null if no conversation)    |
| messages        | MessageInfo[]   | Chronological message list        |

### MessageInfo

| Field      | Type   | Description                     |
| ---------- | ------ | ------------------------------- |
| id         | int    | Message ID                      |
| role       | string | "user" or "assistant"           |
| content    | string | Message text                    |
| created_at | string | ISO 8601 timestamp              |

### Error Responses

| Status | Condition                    | Body                                    |
| ------ | ---------------------------- | --------------------------------------- |
| 401    | Missing/invalid/expired JWT  | `{"detail": "Invalid authentication token"}` |
| 403    | user_id mismatch with JWT    | `{"detail": "Forbidden"}`               |
| 500    | Database error               | `{"detail": "Internal server error"}`   |

### Notes

- Returns empty messages array `[]` if no conversation exists yet.
- Creates no side effects — purely a read operation.

---

## MCP Tool Contracts (Already Implemented)

All 5 tools are in `backend/src/mcp/server.py`. Each returns a
JSON string with `status` ("success" or "error") and tool-specific
data.

### add_task(user_id, title, description?)
- **Input**: user_id (required), title (1-255, required),
  description (0-1000, optional)
- **Output**: `{status, task: {id, title, description, completed, created_at}}`

### list_tasks(user_id)
- **Input**: user_id (required)
- **Output**: `{status, tasks: [{id, title, description, completed, created_at}], count}`

### complete_task(user_id, task_id)
- **Input**: user_id (required), task_id (positive int, required)
- **Output**: `{status, task: {id, title, completed, updated_at}}`

### update_task(user_id, task_id, title?, description?)
- **Input**: user_id (required), task_id (positive int, required),
  title (1-255, optional), description (0-1000, optional);
  at least one field required
- **Output**: `{status, task: {id, title, description, completed, updated_at}}`

### delete_task(user_id, task_id)
- **Input**: user_id (required), task_id (positive int, required)
- **Output**: `{status, message}`
