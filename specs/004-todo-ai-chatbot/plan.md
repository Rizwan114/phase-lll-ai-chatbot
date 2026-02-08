# Implementation Plan: Phase III - Todo AI Chatbot

**Branch**: `004-todo-ai-chatbot` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-todo-ai-chatbot/spec.md`

## Summary

Build an AI-powered Todo chatbot by integrating the OpenAI Agents SDK
with MCP tools on top of the existing FastAPI backend. The agent
orchestrates 5 MCP tools (add_task, list_tasks, complete_task,
update_task, delete_task) to manage tasks via natural language. A new
chat API endpoint serves as the sole frontend integration point. New
Conversation and Message models persist chat state in PostgreSQL. The
ChatKit frontend renders the conversational UI.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, openai-agents, mcp[cli]
**Storage**: Neon Serverless PostgreSQL (SQLModel ORM)
**Testing**: pytest
**Target Platform**: Linux/Windows server (backend), Web browser (frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: <5s response time for chat messages (SC-001)
**Constraints**: Stateless server, all state in PostgreSQL, MCP-only mutations
**Scale/Scope**: Single-user at a time, single conversation per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-First Discipline Check
- [x] All requirements trace back to approved spec (FR-001 through FR-017)
- [x] Feature specification exists and is complete (specs/004-todo-ai-chatbot/spec.md)
- [x] Implementation plan references specific spec sections
- [x] MCP tools, API endpoints, and data models documented in spec

### Stateless Architecture Check
- [x] FastAPI server designed as stateless (no in-memory state)
- [x] All state persisted in PostgreSQL (Neon) only
- [x] AI agents interact with tasks only through MCP tools
- [x] No in-memory state or server-side session storage
- [x] Conversation state reconstructed from database on every request

### Data Integrity and User Isolation Check
- [x] User ownership enforced at MCP tool layer (all tools receive user_id)
- [x] Cross-user data access impossible by design (user_id scoping)
- [x] No hardcoded secrets in implementation plan (env vars only)
- [x] Database schema supports multi-user isolation (user_id on all tables)

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
specs/004-todo-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   ├── chat-api.md      # Chat endpoint contract
│   └── mcp-tools.md     # MCP tool contracts
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py                    # FastAPI app (add chat router)
│   ├── settings.py                # Settings (add OPENAI_API_KEY)
│   ├── models/
│   │   ├── task_model.py          # Existing Task model (unchanged)
│   │   ├── user_model.py          # Existing User model (unchanged)
│   │   ├── conversation_model.py  # NEW: Conversation model
│   │   └── message_model.py       # NEW: Message model
│   ├── services/
│   │   ├── task_service.py        # Existing (unchanged)
│   │   ├── conversation_service.py # NEW: Conversation CRUD
│   │   └── message_service.py     # NEW: Message CRUD
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py              # NEW: MCP server with 5 tools
│   │   └── tools.py               # NEW: MCP tool implementations
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py               # NEW: Agent configuration
│   │   └── runner.py              # NEW: Agent execution runner
│   ├── api/
│   │   ├── task_routes.py         # Existing (unchanged)
│   │   ├── auth_routes.py         # Existing (unchanged)
│   │   └── chat_routes.py         # NEW: POST /api/{user_id}/chat
│   ├── schemas/
│   │   ├── task_schemas.py        # Existing (unchanged)
│   │   └── chat_schemas.py        # NEW: ChatRequest, ChatResponse
│   ├── database/
│   │   └── database.py            # Updated: import new models
│   ├── auth/                      # Existing (unchanged)
│   ├── handlers/                  # Existing (unchanged)
│   └── utils/                     # Existing (unchanged)
├── tests/
│   ├── unit/
│   │   ├── test_conversation_model.py  # NEW
│   │   ├── test_message_model.py       # NEW
│   │   └── test_mcp_tools.py           # NEW
│   └── integration/
│       └── test_chat_api.py            # NEW
└── requirements.txt               # Updated: add openai-agents, mcp[cli]

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx               # NEW: Chat page
│   └── ...                        # Existing (unchanged)
├── components/
│   └── chat/
│       ├── ChatInterface.tsx      # NEW: Chat UI component
│       ├── MessageList.tsx        # NEW: Message display
│       └── MessageInput.tsx       # NEW: Message input form
├── lib/
│   └── api/
│       ├── chat-service.ts        # NEW: Chat API client
│       └── ...                    # Existing (unchanged)
└── ...                            # Existing (unchanged)
```

**Structure Decision**: Web application structure (backend/ + frontend/).
Extends the existing Phase II layout. New files are added within existing
directories. No existing files are deleted. Phase II REST endpoints
remain operational for backward compatibility.

## Architecture

### Request Flow

```
                    ┌─────────────┐
                    │   ChatKit   │
                    │  Frontend   │
                    └──────┬──────┘
                           │ POST /api/{user_id}/chat
                           │ { message, conversation_id? }
                    ┌──────▼──────┐
                    │   FastAPI   │
                    │ chat_routes │
                    └──────┬──────┘
                           │ 1. Load/create conversation
                           │ 2. Load message history
                           │ 3. Persist user message
                    ┌──────▼──────┐
                    │   OpenAI    │
                    │   Agent     │
                    │  (Runner)   │
                    └──────┬──────┘
                           │ Tool calls (0..N)
                    ┌──────▼──────┐
                    │  MCP Server │
                    │  (stdio)    │
                    │             │
                    │ add_task    │
                    │ list_tasks  │
                    │ complete    │
                    │ update      │
                    │ delete      │
                    └──────┬──────┘
                           │ TaskService
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │   (Neon)    │
                    └─────────────┘
```

### Key Design Decisions

1. **MCP Server as stdio subprocess**: The OpenAI Agents SDK launches
   the MCP server via `MCPServerStdio`. The MCP server defines 5 tools
   that call existing `TaskService` methods.

2. **Agent per-request**: Each chat request creates a fresh agent run
   with the full conversation history. No agent state persists between
   requests (stateless architecture).

3. **Conversation model**: One conversation per user (unique constraint
   on user_id). Messages ordered by created_at for history reconstruction.

4. **user_id passthrough**: The chat endpoint extracts user_id from
   the URL path and passes it to MCP tools as a parameter. MCP tools
   never infer user identity — it's always explicit.

5. **Existing code untouched**: Phase II REST endpoints, auth, and task
   service continue to work. Phase III adds new modules alongside.

## Complexity Tracking

No constitution violations. All design decisions comply with the 8
constitutional principles.

## Phase 0: Research Summary

See [research.md](./research.md) for full details.

Key decisions:
- **R1**: OpenAI Agents SDK (`openai-agents`) for agent orchestration
- **R2**: MCP Python SDK (`mcp[cli]`) with stdio transport
- **R3**: Conversation + Message models in PostgreSQL
- **R4**: Single chat endpoint `POST /api/{user_id}/chat`
- **R5**: ChatKit frontend component
- **R6**: MCP tools wrap existing TaskService methods
- **R7**: Better Auth provides user_id (existing Phase II)

## Phase 1: Design Summary

### Data Model
See [data-model.md](./data-model.md) — 3 canonical models: Task
(existing), Conversation (new), Message (new).

### API Contracts
See [contracts/chat-api.md](./contracts/chat-api.md) — Chat endpoint.
See [contracts/mcp-tools.md](./contracts/mcp-tools.md) — 5 MCP tools.

### Quickstart
See [quickstart.md](./quickstart.md) — Setup and verification guide.

## Implementation Layers (for /sp.tasks)

The implementation MUST proceed in this order:

### Layer 1: Database Models (no dependencies)
- Conversation model + Message model
- Database registration (import in database.py)
- Table creation on startup

### Layer 2: Services (depends on Layer 1)
- ConversationService: get_or_create, get_by_id
- MessageService: create, list_by_conversation

### Layer 3: MCP Server (depends on Layer 2)
- MCP server definition with 5 tools
- Each tool wraps TaskService with user_id validation
- Structured input/output per contracts/mcp-tools.md

### Layer 4: Agent (depends on Layer 3)
- Agent configuration with system prompt
- MCPServerStdio connection to MCP server
- Runner execution with conversation history

### Layer 5: Chat API (depends on Layers 2 + 4)
- ChatRequest/ChatResponse schemas
- POST /api/{user_id}/chat endpoint
- Conversation management + agent execution
- Router registration in main.py

### Layer 6: Frontend (depends on Layer 5)
- Chat service (API client)
- Chat UI components
- Chat page
- Navigation integration

### Layer 7: Validation (depends on all)
- End-to-end testing
- Constitutional compliance verification
