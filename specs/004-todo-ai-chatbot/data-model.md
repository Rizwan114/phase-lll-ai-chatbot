# Data Model: Phase III - Todo AI Chatbot

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-08
**ORM**: SQLModel (SQLAlchemy + Pydantic)
**Database**: Neon Serverless PostgreSQL

## Canonical Models

These models are authoritative and MUST NOT drift from this specification.
No additional fields or models may be introduced without explicit approval.

### Task (existing — Phase II, retained)

Represents a single todo item belonging to a user.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | Integer | PK, auto-increment | Unique task identifier |
| user_id | String(255) | NOT NULL, indexed | Owner reference |
| title | String(255) | NOT NULL, min 1 char | Task title |
| description | String(1000) | Nullable | Optional details |
| completed | Boolean | NOT NULL, default false | Completion status |
| created_at | DateTime | NOT NULL, default now() | Creation timestamp |
| updated_at | DateTime | NOT NULL, default now() | Last modification |

**Indexes**: `(user_id)` for ownership queries.

**Validation rules**:
- title MUST be 1–255 characters
- description MUST be 0–1000 characters if provided
- user_id MUST be non-empty

**State transitions**:
- `created` → `completed` (via complete_task MCP tool)
- `completed` → `created` (via complete_task toggle)
- Any state → `deleted` (via delete_task MCP tool)

### Conversation (new)

Represents a chat session for a user. Each user has at most one
active conversation.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | String(UUID) | PK, UUID default | Unique conversation ID |
| user_id | String(255) | NOT NULL, indexed, unique | Owner (one conversation per user) |
| created_at | DateTime | NOT NULL, default now() | Creation timestamp |
| updated_at | DateTime | NOT NULL, default now() | Last message timestamp |

**Indexes**: `(user_id)` unique for single-conversation-per-user lookup.

**Validation rules**:
- user_id MUST be non-empty
- Only one conversation per user_id (unique constraint)

**Relationships**:
- Has many Messages (cascade delete)

### Message (new)

Represents a single message in a conversation.

| Field | Type | Constraints | Notes |
|---|---|---|---|
| id | Integer | PK, auto-increment | Unique message ID |
| conversation_id | String(UUID) | FK → Conversation.id, NOT NULL | Parent conversation |
| user_id | String(255) | NOT NULL | Message sender/owner |
| role | String(20) | NOT NULL, enum: user/assistant | Message author role |
| content | Text | NOT NULL | Message text content |
| created_at | DateTime | NOT NULL, default now() | Message timestamp |

**Indexes**: `(conversation_id, created_at)` for ordered history retrieval.

**Validation rules**:
- role MUST be one of: "user", "assistant"
- content MUST be non-empty
- conversation_id MUST reference an existing Conversation

**Relationships**:
- Belongs to one Conversation

## Entity Relationship Diagram

```
User (existing)
  │
  ├── 1:N ── Task
  │           (user_id FK)
  │
  └── 1:1 ── Conversation
              (user_id FK, unique)
              │
              └── 1:N ── Message
                          (conversation_id FK)
```

## Migration Notes

### New tables to create:
1. `conversation` — with UUID primary key, unique user_id
2. `message` — with FK to conversation, ordered by created_at

### Existing table changes:
- `task` — No schema changes. Existing Phase II table is retained as-is.

### Migration strategy:
- SQLModel `create_all()` handles table creation on startup
- No data migration needed (Phase III adds new tables only)
- Backward compatible: Phase II REST endpoints continue to work

## Query Patterns

### Get or create conversation for user:
```
SELECT * FROM conversation WHERE user_id = :user_id
-- If not found:
INSERT INTO conversation (id, user_id, created_at, updated_at)
VALUES (:uuid, :user_id, now(), now())
```

### Load conversation history:
```
SELECT role, content FROM message
WHERE conversation_id = :conversation_id
ORDER BY created_at ASC
```

### Persist new message:
```
INSERT INTO message (conversation_id, user_id, role, content, created_at)
VALUES (:conversation_id, :user_id, :role, :content, now())
```

### Update conversation timestamp:
```
UPDATE conversation SET updated_at = now()
WHERE id = :conversation_id
```
