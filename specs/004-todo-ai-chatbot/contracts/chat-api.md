# Chat API Contract

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-08

## POST /api/{user_id}/chat

The single integration point between frontend and agent backend.

### Path Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| user_id | string | Yes | Authenticated user identifier |

### Request Body

```json
{
  "conversation_id": "string (UUID, optional)",
  "message": "string (required, 1-10000 chars)"
}
```

| Field | Type | Required | Constraints | Description |
|---|---|---|---|---|
| conversation_id | string (UUID) | No | Valid UUID if provided | Existing conversation to continue. If omitted, a new conversation is created. |
| message | string | Yes | 1–10,000 characters | Natural language user message |

### Response Body (200 OK)

```json
{
  "conversation_id": "string (UUID)",
  "response": "string",
  "tool_calls": [
    {
      "tool": "string",
      "input": {},
      "output": {}
    }
  ]
}
```

| Field | Type | Always Present | Description |
|---|---|---|---|
| conversation_id | string (UUID) | Yes | The conversation ID (new or existing) |
| response | string | Yes | Agent's natural language response |
| tool_calls | array | No | Optional list of MCP tools invoked |

### Tool Call Object

```json
{
  "tool": "add_task",
  "input": { "title": "buy groceries" },
  "output": { "id": 1, "title": "buy groceries", "completed": false }
}
```

### Error Responses

| Status | Condition | Body |
|---|---|---|
| 400 | Empty message or invalid input | `{ "detail": "Message is required" }` |
| 401 | Missing or invalid authentication | `{ "detail": "Not authenticated" }` |
| 403 | user_id mismatch with auth token | `{ "detail": "Forbidden" }` |
| 404 | conversation_id not found for user | `{ "detail": "Conversation not found" }` |
| 422 | Validation error | `{ "detail": [{ "loc": [...], "msg": "...", "type": "..." }] }` |
| 500 | Agent or database error | `{ "detail": "Internal server error" }` |

### Behavior Contract

1. If `conversation_id` is omitted, create a new Conversation.
2. If `conversation_id` is provided, verify it belongs to `user_id`.
3. Load all Messages for the conversation, ordered by created_at.
4. Persist the user message to the Message table.
5. Construct agent message history from database messages.
6. Run the AI agent with conversation history and MCP tools.
7. Persist the agent's response as an assistant Message.
8. Update the Conversation's updated_at timestamp.
9. Return the response with conversation_id and optional tool_calls.

### Idempotency

- Not idempotent. Each POST creates new messages.
- Duplicate messages from the same user are accepted (no dedup).

### Concurrency

- Concurrent requests for the same user are handled via database-level
  consistency (PostgreSQL row locking on conversation).
- No server-side mutex or session locks.
