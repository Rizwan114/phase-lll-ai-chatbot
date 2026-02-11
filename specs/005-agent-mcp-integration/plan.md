# Implementation Plan: AI Agent, MCP Orchestration & Frontend Integration

**Branch**: `005-agent-mcp-integration` | **Date**: 2026-02-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-agent-mcp-integration/spec.md`

## Summary

This feature connects the existing AI agent backend (OpenAI Agents SDK +
MCP tools + chat endpoint) with a new frontend chat interface. The backend
is fully implemented: agent, 5 MCP tools, chat endpoint, conversation and
message persistence. The work focuses on: (1) adding a conversation history
endpoint, (2) hardening backend error handling and input validation, and
(3) building the frontend chat page with message rendering and tool
activity indicators.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Next.js 16+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, MCP (FastMCP), Next.js App Router, React 18+
**Storage**: Neon Serverless PostgreSQL (via SQLModel ORM)
**Testing**: Manual end-to-end verification via quickstart checklist
**Target Platform**: Web (server: Linux/Windows, client: modern browsers)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: Chat response within 5 seconds (SC-001)
**Constraints**: Stateless backend, database-only state, MCP-only mutations
**Scale/Scope**: Single-user development; multi-user by design

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-First Discipline Check
- [x] All requirements trace back to approved spec
- [x] Feature specification exists and is complete
- [x] Implementation plan references specific spec sections
- [x] MCP tools, API endpoints, and data models documented in spec

### Stateless Architecture Check
- [x] FastAPI server designed as stateless
- [x] All state persisted in PostgreSQL (Neon) only
- [x] AI agents interact with tasks only through MCP tools
- [x] No in-memory state or server-side session storage
- [x] Conversation state reconstructed from database on every request

### Data Integrity and User Isolation Check
- [x] User ownership enforced at MCP tool layer
- [x] Cross-user data access impossible by design
- [x] No hardcoded secrets in implementation plan
- [x] Database schema supports multi-user isolation

### Tech Stack Compliance Check
- [x] Uses only approved stack (FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, MCP)
- [x] No unauthorized technology deviations
- [x] Dependencies align with constitutional requirements

### MCP Tool Contract Check
- [x] Only approved MCP tools used (add_task, list_tasks, complete_task, update_task, delete_task)
- [x] Tools validate input and enforce user ownership
- [x] Tools return structured, predictable output
- [x] Error responses are explicit and machine-readable

### AI Agent Behavior Check
- [x] Agent uses OpenAI Agents SDK
- [x] Agent selects MCP tools based on user intent
- [x] Multi-step reasoning planned where required
- [x] Agent never hallucinated task IDs or fabricates outputs

### Agentic Workflow Check
- [x] Plan assumes agent-generated code (no manual coding)
- [x] Follows Read Spec → Plan → Tasks → Implement → Validate order
- [x] Automated testing strategy included

## Project Structure

### Documentation (this feature)

```text
specs/005-agent-mcp-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── chat-api.md      # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agent/
│   │   ├── agent.py           # Agent config + system prompt [EXISTS]
│   │   └── runner.py          # Async agent runner [EXISTS]
│   ├── api/
│   │   ├── chat_routes.py     # POST /chat [EXISTS] + GET /chat/history [NEW]
│   │   ├── task_routes.py     # Task CRUD routes [EXISTS]
│   │   └── auth_routes.py     # Auth routes [EXISTS]
│   ├── mcp/
│   │   └── server.py          # 5 MCP tools [EXISTS]
│   ├── models/
│   │   ├── conversation_model.py  [EXISTS]
│   │   ├── message_model.py       [EXISTS]
│   │   └── task_model.py          [EXISTS]
│   ├── schemas/
│   │   └── chat_schemas.py    # Request/Response schemas [EXISTS, MODIFY]
│   ├── services/
│   │   ├── conversation_service.py  [EXISTS]
│   │   └── message_service.py       [EXISTS]
│   ├── database/
│   │   └── database.py        [EXISTS]
│   ├── auth/
│   │   └── middleware.py       [EXISTS]
│   └── main.py                [EXISTS]
└── requirements.txt           [EXISTS]

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx           # Chat page [NEW]
│   ├── dashboard/
│   │   └── page.tsx           [EXISTS]
│   ├── layout.tsx             [EXISTS]
│   └── providers.tsx          [EXISTS]
├── components/
│   ├── chat/
│   │   ├── ChatInterface.tsx  # Chat orchestrator [NEW]
│   │   ├── MessageList.tsx    # Message display [NEW]
│   │   ├── MessageBubble.tsx  # Single message [NEW]
│   │   ├── MessageInput.tsx   # Text input + send [NEW]
│   │   └── ToolCallBadge.tsx  # Tool activity indicator [NEW]
│   ├── layout/
│   │   └── Header.tsx         [EXISTS, MODIFY — add Chat nav link]
│   ├── tasks/                 [EXISTS, NO CHANGE]
│   └── ui/                    [EXISTS, NO CHANGE]
├── lib/
│   ├── api/
│   │   ├── api-client.ts      [EXISTS, NO CHANGE]
│   │   ├── chat-service.ts    # Chat API client [NEW]
│   │   ├── task-service.ts    [EXISTS, NO CHANGE]
│   │   └── types.ts           [EXISTS, MODIFY — add chat types]
│   └── auth/
│       └── auth-context.tsx   [EXISTS, NO CHANGE]
└── package.json               [EXISTS, NO CHANGE]
```

**Structure Decision**: Web application structure (backend/ + frontend/)
matching the existing repository layout. No new directories beyond
`frontend/app/chat/` and `frontend/components/chat/`.

## Implementation Architecture

### Backend Changes (Minimal)

The backend is ~95% complete. Changes needed:

1. **New endpoint**: `GET /api/{user_id}/chat/history` in
   `chat_routes.py` — returns conversation messages for page load
   (FR-014 support).

2. **New schemas**: `MessageInfo` and `ChatHistoryResponse` in
   `chat_schemas.py` — typed response for the history endpoint.

3. **Input validation hardening**: Add explicit message length
   validation error messages in `chat_routes.py` for empty and
   overlength messages (FR-016 support).

4. **Error response improvement**: Wrap agent failures with
   user-friendly messages instead of generic 500 (FR-007 support).

### Frontend Changes (Primary Focus)

New chat feature built from scratch:

1. **Chat service** (`lib/api/chat-service.ts`): API client for
   POST /chat and GET /chat/history, following task-service pattern.

2. **Chat types** (`lib/api/types.ts`): Add ChatMessage,
   ToolCallInfo, ChatResponse, ChatHistoryResponse interfaces.

3. **Chat page** (`app/chat/page.tsx`): Auth-guarded page with
   Header + ChatInterface. Same pattern as dashboard page.

4. **ChatInterface** (`components/chat/ChatInterface.tsx`):
   State manager — loads history, sends messages, appends
   responses, manages loading/error states.

5. **MessageList** (`components/chat/MessageList.tsx`):
   Scrollable container rendering MessageBubble for each message.
   Auto-scrolls to bottom on new messages.

6. **MessageBubble** (`components/chat/MessageBubble.tsx`):
   User messages right-aligned, assistant messages left-aligned.
   Shows ToolCallBadge when tool_calls present.

7. **MessageInput** (`components/chat/MessageInput.tsx`):
   Text input with send button. Validates non-empty, shows
   loading state while waiting for response.

8. **ToolCallBadge** (`components/chat/ToolCallBadge.tsx`):
   Small badge/pill showing tool name (e.g., "add_task") when
   the agent invoked an MCP tool.

9. **Header update** (`components/layout/Header.tsx`):
   Add "Chat" navigation link next to existing logo/title.

### Data Flow

```
User types message
  → MessageInput.onSubmit()
  → ChatInterface.handleSend()
  → chatService.sendMessage(userId, message)
  → POST /api/{user_id}/chat
  → Backend: auth → conversation → history → agent → persist → respond
  → ChatResponse { conversation_id, response, tool_calls? }
  → ChatInterface appends assistant message to state
  → MessageList re-renders with new MessageBubble
  → ToolCallBadge shows if tool_calls present
```

### Page Load Flow

```
User navigates to /chat
  → ChatInterface.useEffect()
  → chatService.getHistory(userId)
  → GET /api/{user_id}/chat/history
  → ChatHistoryResponse { conversation_id, messages[] }
  → ChatInterface sets messages state
  → MessageList renders all historical messages
```

## Complexity Tracking

> No constitutional violations. All changes follow existing patterns.

| Decision | Rationale |
|----------|-----------|
| New GET endpoint | Needed for FR-014 (load history on page open); POST-only would require sending empty messages |
| No streaming | Out of scope per spec; complete response approach is simpler and stateless |
| Separate chat page | Dashboard is task-list focused; chat is a distinct interaction mode |

## Implementation Order

1. **Backend**: Add history endpoint + schema updates (small, unblocks frontend)
2. **Frontend types + service**: Add chat types and API client
3. **Frontend components**: Build from innermost (ToolCallBadge, MessageBubble) outward (MessageList, MessageInput, ChatInterface)
4. **Frontend page + navigation**: Wire up chat page and Header link
5. **Validation**: End-to-end testing per quickstart checklist

## Risks and Mitigations

1. **Agent latency**: GPT-4o-mini via MCP subprocess may exceed 5s target.
   **Mitigation**: Show loading indicator immediately; the 5s target is
   a goal, not a hard constraint.

2. **MCP subprocess reliability**: stdio transport could fail silently.
   **Mitigation**: Existing try/catch in runner.py returns error;
   chat_routes.py wraps in 500 handler. Frontend shows friendly error.

3. **Conversation history growth**: Very long conversations may slow
   agent processing (all history sent per request).
   **Mitigation**: Not a launch concern for MVP. Future: truncation
   or summarization strategy.
