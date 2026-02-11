# Data Model: AI Agent, MCP Orchestration & Frontend Integration

**Branch**: `005-agent-mcp-integration` | **Date**: 2026-02-11

## Existing Entities (No Changes Required)

All entities below are already implemented in the codebase. This
document confirms they meet spec requirements.

### Conversation

**File**: `backend/src/models/conversation_model.py`

| Field      | Type     | Constraints                        |
| ---------- | -------- | ---------------------------------- |
| id         | str/UUID | PK, auto-generated UUID            |
| user_id    | str      | unique, indexed, 1-255 chars       |
| created_at | datetime | auto-set on creation               |
| updated_at | datetime | auto-set, updated on each message  |

**Relationships**: One-to-many with Message.
**Constraint**: One conversation per user (unique on user_id).

### Message

**File**: `backend/src/models/message_model.py`

| Field           | Type     | Constraints                    |
| --------------- | -------- | ------------------------------ |
| id              | int      | PK, auto-increment             |
| conversation_id | str      | FK → Conversation.id, indexed  |
| user_id         | str      | 1-255 chars                    |
| role            | str      | "user" or "assistant", 1-20    |
| content         | str      | min_length=1                   |
| created_at      | datetime | auto-set on creation           |

**Relationships**: Many-to-one with Conversation.

### Task

**File**: `backend/src/models/task_model.py`

| Field       | Type     | Constraints                   |
| ----------- | -------- | ----------------------------- |
| id          | int      | PK, auto-increment            |
| title       | str      | 1-255 chars, required         |
| description | str      | 0-1000 chars, optional        |
| completed   | bool     | default False                 |
| user_id     | str      | 1-255 chars                   |
| created_at  | datetime | auto-set                      |
| updated_at  | datetime | auto-set                      |

**Managed exclusively via MCP tools** — the agent never accesses
this table directly.

## Frontend Types (New)

### ChatMessage (frontend type)

```typescript
interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  created_at: string;
  tool_calls?: ToolCallInfo[];
}
```

### ToolCallInfo (frontend type)

```typescript
interface ToolCallInfo {
  tool: string;
  input: unknown;
  output?: unknown;
}
```

### ChatResponse (frontend type)

```typescript
interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: ToolCallInfo[];
}
```

### ChatHistoryResponse (frontend type, new endpoint)

```typescript
interface ChatHistoryResponse {
  conversation_id: string;
  messages: ChatMessage[];
}
```

## Entity Relationship Diagram

```
User (1) ──── (1) Conversation ──── (*) Message
  │
  └──── (*) Task (via MCP tools only)
```

## Validation Rules Summary

- **Conversation**: One per user. Auto-created on first chat.
- **Message**: Content required (min 1 char). Role must be
  "user" or "assistant". Ordered by created_at within
  conversation.
- **Task**: Title required (1-255). Description optional
  (max 1000). User ownership enforced at MCP tool layer.
- **ChatRequest**: Message min 1 char, max 10000 chars.
