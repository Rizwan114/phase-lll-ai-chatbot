# Tasks: Phase III - Todo AI Chatbot

**Input**: Design documents from `/specs/004-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in the feature specification. Tests omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/`
- Paths use the existing Phase II structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add Phase III dependencies and configuration

- [x] T001 Add `openai-agents` and `mcp[cli]` to `backend/requirements.txt`
- [x] T002 Add `OPENAI_API_KEY` setting to `backend/src/settings.py` and `backend/.env.example`
- [x] T003 [P] Create `backend/src/mcp/__init__.py` empty init module
- [x] T004 [P] Create `backend/src/agent/__init__.py` empty init module

**Checkpoint**: Dependencies installed, directory structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models, services, and MCP server that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create Conversation model in `backend/src/models/conversation_model.py` per data-model.md (UUID PK, unique user_id, timestamps)
- [x] T006 [P] Create Message model in `backend/src/models/message_model.py` per data-model.md (FK to Conversation, role enum, content text, timestamps)
- [x] T007 Register Conversation and Message model imports in `backend/src/database/database.py` so tables auto-create on startup
- [x] T008 [P] Create ConversationService in `backend/src/services/conversation_service.py` with get_or_create(user_id) and get_by_id(conversation_id, user_id) methods
- [x] T009 [P] Create MessageService in `backend/src/services/message_service.py` with create(conversation_id, user_id, role, content) and list_by_conversation(conversation_id) methods
- [x] T010 Implement MCP server with `add_task` tool in `backend/src/mcp/server.py` using `mcp` SDK and `@server.tool()` decorator wrapping TaskService.create_task() per contracts/mcp-tools.md
- [x] T011 Add `list_tasks` tool to MCP server in `backend/src/mcp/server.py` wrapping TaskService.get_tasks_by_user() per contracts/mcp-tools.md
- [x] T012 Add `complete_task` tool to MCP server in `backend/src/mcp/server.py` wrapping TaskService.toggle_task_completion() per contracts/mcp-tools.md
- [x] T013 Add `update_task` tool to MCP server in `backend/src/mcp/server.py` wrapping TaskService.update_task() per contracts/mcp-tools.md
- [x] T014 Add `delete_task` tool to MCP server in `backend/src/mcp/server.py` wrapping TaskService.delete_task() per contracts/mcp-tools.md
- [x] T015 Configure OpenAI Agent in `backend/src/agent/agent.py` with system prompt for task management and MCPServerStdio connection to `backend.src.mcp.server`
- [x] T016 Implement agent runner in `backend/src/agent/runner.py` with run(messages, user_id) method that creates Agent, passes conversation history, and returns RunResult with final_output and tool_calls
- [x] T017 [P] Create ChatRequest and ChatResponse Pydantic schemas in `backend/src/schemas/chat_schemas.py` per contracts/chat-api.md
- [x] T018 Implement POST /api/{user_id}/chat endpoint in `backend/src/api/chat_routes.py` that: (1) gets/creates conversation, (2) loads message history, (3) persists user message, (4) runs agent, (5) persists assistant response, (6) returns ChatResponse per contracts/chat-api.md
- [x] T019 Register chat_routes router in `backend/src/main.py` with prefix `/api` and update app description for Phase III
- [x] T020 Add auth middleware to chat endpoint in `backend/src/api/chat_routes.py` using existing Better Auth JWT validation from `backend/src/auth/middleware.py`

**Checkpoint**: Foundation ready — full backend pipeline works: chat message → agent → MCP tool → database → response. User story implementation can now begin.

---

## Phase 3: User Story 1 + 2 — Add & List Tasks via Chat (Priority: P1) MVP

**Goal**: Users can add tasks and list their tasks via natural language chat messages. This proves the full end-to-end pipeline.

**Independent Test**: Send "Add a task to buy groceries" and verify task created. Send "Show my tasks" and verify task listed.

### Implementation for User Story 1 + 2

- [ ] T021 [US1] Verify add_task MCP tool handles natural language title extraction — test by sending POST to /api/{user_id}/chat with message "Add a task to buy groceries" and confirming task in database
- [ ] T022 [US2] Verify list_tasks MCP tool returns readable task list — test by adding tasks then sending "Show my tasks" and confirming all tasks returned
- [ ] T023 [US1] Verify add_task handles optional description — test with "Add task: finish report. Description: due by Friday"
- [ ] T024 [US2] Verify list_tasks handles empty list — test with new user sending "List my tasks" and confirming friendly empty response
- [ ] T025 [US1][US2] Verify agent confirms actions in natural language — add task then list, confirm both responses are human-readable confirmations

**Checkpoint**: At this point, users can add and view tasks via chat. MVP is functional.

---

## Phase 4: User Story 3 — Complete a Task via Chat (Priority: P2)

**Goal**: Users can mark tasks as completed by telling the chatbot they finished a task.

**Independent Test**: Add a task, send "I finished buying groceries", verify task marked completed.

### Implementation for User Story 3

- [ ] T026 [US3] Verify complete_task MCP tool marks task as completed — test by adding task, sending completion message, confirming completed=true in database
- [ ] T027 [US3] Verify complete_task handles task-not-found — send "Complete task 999" and confirm friendly error response
- [ ] T028 [US3] Verify agent resolves task by name — send "Mark buy groceries as done" and confirm correct task identified and completed

**Checkpoint**: Users can now add, list, and complete tasks via chat.

---

## Phase 5: User Story 4 — Update a Task via Chat (Priority: P2)

**Goal**: Users can modify task titles or descriptions via chat.

**Independent Test**: Add a task, send "Change buy groceries to buy groceries and snacks", verify title updated.

### Implementation for User Story 4

- [ ] T029 [US4] Verify update_task MCP tool updates title — test by adding task, sending update message, confirming new title in database
- [ ] T030 [US4] Verify update_task handles task-not-found — send update for non-existent task and confirm friendly error
- [ ] T031 [US4] Verify update_task validates at least one field provided — confirm error when no title or description given

**Checkpoint**: Users can add, list, complete, and update tasks via chat.

---

## Phase 6: User Story 5 — Delete a Task via Chat (Priority: P2)

**Goal**: Users can delete tasks via chat, including bulk operations.

**Independent Test**: Add a task, send "Delete the groceries task", verify task removed from database.

### Implementation for User Story 5

- [ ] T032 [US5] Verify delete_task MCP tool deletes task — test by adding task, sending delete message, confirming task removed from database
- [ ] T033 [US5] Verify delete_task handles task-not-found — send delete for non-existent task and confirm friendly error
- [ ] T034 [US5] Verify agent handles bulk delete via multi-step reasoning — add 3 completed tasks, send "Delete all completed tasks", confirm agent lists then deletes each

**Checkpoint**: Full CRUD lifecycle complete via chat. All P2 stories done.

---

## Phase 7: User Story 6 — Conversation Persistence (Priority: P3)

**Goal**: Conversations survive server restarts by reconstructing from database.

**Independent Test**: Send messages, restart server (new request), send follow-up referencing prior context, verify agent has full history.

### Implementation for User Story 6

- [ ] T035 [US6] Verify conversation auto-creation — send first message without conversation_id, confirm new conversation created and ID returned
- [ ] T036 [US6] Verify conversation continuity — send multiple messages with same conversation_id, confirm agent references prior context
- [ ] T037 [US6] Verify history reconstruction from database — send messages, confirm all messages persisted, start fresh request with same conversation_id, confirm full history loaded
- [ ] T038 [US6] Verify conversation ownership — attempt to use another user's conversation_id, confirm 404 error

**Checkpoint**: Stateless architecture validated — conversations persist across restarts.

---

## Phase 8: User Story 7 — Multi-Step Agent Reasoning (Priority: P3)

**Goal**: Agent chains multiple MCP tool calls for complex requests.

**Independent Test**: Create 3 completed + 2 incomplete tasks, send "Delete all completed tasks", verify 3 deletions.

### Implementation for User Story 7

- [ ] T039 [US7] Verify multi-step: list then delete — add completed tasks, send "Delete all completed tasks", confirm agent calls list_tasks then delete_task for each
- [ ] T040 [US7] Verify multi-step: list then count — add tasks, send "How many tasks do I have left?", confirm agent lists and counts

**Checkpoint**: All user stories complete. Agent handles both single and multi-step operations.

---

## Phase 9: Frontend Integration

**Purpose**: Connect ChatKit UI to backend chat API

- [ ] T041 [P] Install `@openai/chat-kit` package in `frontend/` via npm
- [ ] T042 [P] Create chat API client in `frontend/lib/api/chat-service.ts` with sendMessage(userId, message, conversationId?) method calling POST /api/{user_id}/chat
- [ ] T043 Create ChatInterface component in `frontend/components/chat/ChatInterface.tsx` using ChatKit with message list and input
- [ ] T044 Create MessageList component in `frontend/components/chat/MessageList.tsx` rendering conversation messages with role-based styling
- [ ] T045 Create MessageInput component in `frontend/components/chat/MessageInput.tsx` with text input and send button
- [ ] T046 Create chat page at `frontend/app/chat/page.tsx` composing ChatInterface with auth protection and conversation state
- [ ] T047 Add navigation link to chat page in `frontend/components/layout/Header.tsx`

**Checkpoint**: Frontend renders chat UI, sends messages to backend, displays agent responses.

---

## Phase 10: Error Handling & Edge Cases

**Purpose**: Harden error handling across all layers

- [ ] T048 Add empty message validation in chat endpoint — return 400 with "Message is required" per contracts/chat-api.md
- [ ] T049 Add message length validation (max 10,000 chars) in chat endpoint — return 400 with length error
- [ ] T050 Add error handling for database unreachable in chat endpoint — return 500 with explicit error, no silent crash
- [ ] T051 Add error handling for MCP tool unexpected errors in agent runner — surface user-friendly error without exposing internals
- [ ] T052 Verify agent responds conversationally to non-task messages without invoking MCP tools

**Checkpoint**: All edge cases from spec handled gracefully.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [ ] T053 Verify no hardcoded secrets in codebase — scan for API keys, passwords, tokens in all modified files
- [ ] T054 Verify CORS settings allow frontend origin in `backend/src/main.py`
- [ ] T055 Run full end-to-end flow: add task → list tasks → complete task → update task → delete task → verify conversation persists
- [ ] T056 Verify user isolation — create tasks as user A, attempt to list/modify as user B, confirm 0 results or error
- [ ] T057 Verify Phase II REST endpoints still work (backward compatibility) — GET /api/{user_id}/tasks, POST /api/{user_id}/tasks

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phases 3–8)**: All depend on Foundational phase completion
  - Phases 3–8 MUST proceed sequentially (each builds on prior verification)
- **Frontend (Phase 9)**: Depends on Foundational phase; can run in parallel with Phases 4–8
- **Error Handling (Phase 10)**: Depends on Foundational phase
- **Polish (Phase 11)**: Depends on all prior phases

### Within Each User Story

- Models before services (Phase 2 handles this for all stories)
- MCP tools before agent (Phase 2 handles this)
- Agent before chat endpoint (Phase 2 handles this)
- Verification tasks within each story are sequential

### Parallel Opportunities

- T003 + T004: Init modules (different directories)
- T005 + T006: Models (different files)
- T008 + T009: Services (different files)
- T017 + any model/service task: Schemas (different file)
- T041 + T042: Frontend setup (different operations)
- Phase 9 (Frontend) can run in parallel with Phases 4–8

---

## Parallel Example: Phase 2 Foundation

```bash
# Batch 1: Models (parallel)
Task: T005 "Create Conversation model in backend/src/models/conversation_model.py"
Task: T006 "Create Message model in backend/src/models/message_model.py"

# Batch 2: Registration (depends on Batch 1)
Task: T007 "Register model imports in backend/src/database/database.py"

# Batch 3: Services (parallel, depends on Batch 2)
Task: T008 "Create ConversationService in backend/src/services/conversation_service.py"
Task: T009 "Create MessageService in backend/src/services/message_service.py"

# Batch 4: MCP tools (sequential, depends on Batch 2 for DB access)
Task: T010 "Implement MCP server with add_task tool"
Task: T011-T014 "Add remaining MCP tools"

# Batch 5: Agent (depends on Batch 4)
Task: T015 "Configure OpenAI Agent"
Task: T016 "Implement agent runner"

# Batch 6: Chat API (depends on Batches 3 + 5)
Task: T017 "Create chat schemas" (can parallel with Batch 4-5)
Task: T018 "Implement chat endpoint"
Task: T019 "Register router in main.py"
Task: T020 "Add auth middleware"
```

---

## Implementation Strategy

### MVP First (Phases 1–3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Stories 1 + 2 (Add + List tasks)
4. **STOP and VALIDATE**: Test add + list via chat independently
5. Deploy/demo if ready — this is a working MVP

### Incremental Delivery

1. Phases 1–3 → Foundation + Add/List tasks (MVP!)
2. Phase 4 → Complete tasks → Deploy/Demo
3. Phase 5 → Update tasks → Deploy/Demo
4. Phase 6 → Delete tasks → Full CRUD → Deploy/Demo
5. Phase 7 → Conversation persistence → Stateless validation
6. Phase 8 → Multi-step reasoning → Agent intelligence
7. Phase 9 → Frontend integration → Full UI
8. Phases 10–11 → Hardening → Production ready

---

## Constitutional Compliance Validation

### Spec-First Discipline Tasks
- [ ] T058 Verify all implemented features trace back to approved spec requirements (FR-001 through FR-017)
- [ ] T059 Confirm MCP tool behavior matches spec-defined contract (contracts/mcp-tools.md)
- [ ] T060 Validate that no code was manually written outside agent-generated outputs

### Stateless Architecture Validation Tasks
- [ ] T061 Verify FastAPI server is stateless (no in-memory state between requests)
- [ ] T062 Confirm all state persisted in PostgreSQL (Neon) only
- [ ] T063 Validate conversation state reconstructed from database on every request
- [ ] T064 Test conversation continuity survives server restarts

### Data Integrity and User Isolation Tasks
- [ ] T065 Verify cross-user data access is impossible via MCP tools
- [ ] T066 Confirm user ownership enforced at MCP tool layer
- [ ] T067 Validate database schema supports multi-user isolation
- [ ] T068 Verify no secrets are hardcoded in the codebase

### MCP Tool Contract Validation Tasks
- [ ] T069 Confirm only approved MCP tools used (add_task, list_tasks, complete_task, update_task, delete_task)
- [ ] T070 Verify all tools validate input before processing
- [ ] T071 Test that tools return structured, predictable output
- [ ] T072 Validate error responses are explicit and machine-readable

### AI Agent Behavior Validation Tasks
- [ ] T073 Verify agent uses OpenAI Agents SDK
- [ ] T074 Test multi-step reasoning (e.g., list → delete)
- [ ] T075 Confirm agent never hallucinated task IDs or fabricates outputs
- [ ] T076 Validate agent confirms successful actions in natural language

### Tech Stack Compliance Tasks
- [ ] T077 Confirm all components use approved stack (FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, MCP)
- [ ] T078 Verify stateless server design (no shared sessions or in-memory state)

### Success Criteria Validation Tasks
- [ ] T079 Test end-to-end flow: chat message → MCP tool selection → execution → natural language response
- [ ] T080 Verify each user can only see and modify their own tasks
- [ ] T081 Test multi-step agent reasoning works correctly
- [ ] T082 Confirm all specs pass implementation review without deviation

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitutional compliance tasks must be completed to ensure adherence to project principles
- Phase 2 is the heaviest phase (16 tasks) — it builds the entire backend pipeline
- User story phases (3–8) are lighter — they verify the pipeline works for each operation
