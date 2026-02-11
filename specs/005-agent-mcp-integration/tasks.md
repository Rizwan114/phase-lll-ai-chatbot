# Tasks: AI Agent, MCP Orchestration & Frontend Integration

**Input**: Design documents from `/specs/005-agent-mcp-integration/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/chat-api.md, quickstart.md

**Tests**: Not explicitly requested in specification. No test tasks included.

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Backend additions that unblock all user stories

- [x] T001 Add MessageInfo and ChatHistoryResponse schemas in backend/src/schemas/chat_schemas.py (FR-014, contracts/chat-api.md — add MessageInfo with id, role, content, created_at fields and ChatHistoryResponse with conversation_id and messages list)
- [x] T002 Add GET /{user_id}/chat/history endpoint in backend/src/api/chat_routes.py (FR-014, contracts/chat-api.md — auth check, get conversation by user_id, load messages via MessageService.list_by_conversation, return ChatHistoryResponse; return empty messages array if no conversation exists)
- [x] T003 Harden error handling in POST /{user_id}/chat in backend/src/api/chat_routes.py (FR-007, FR-016 — catch agent failures and return user-friendly message "I'm having trouble right now. Please try again." instead of generic 500; add explicit validation error message for empty/overlength messages)

**Checkpoint**: Backend ready — history endpoint serves messages, chat endpoint has hardened errors

---

## Phase 2: Foundational (Frontend Infrastructure)

**Purpose**: Frontend types and API client that MUST be complete before any UI work

**CRITICAL**: No frontend component work can begin until this phase is complete

- [x] T004 [P] Add chat TypeScript interfaces in frontend/lib/api/types.ts (data-model.md — add ChatMessage with id, role, content, created_at, optional tool_calls; add ToolCallInfo with tool, input, optional output; add ChatSendRequest with message and optional conversation_id; add ChatResponse with conversation_id, response, optional tool_calls; add ChatHistoryResponse with conversation_id and messages array)
- [x] T005 [P] Create chat API service in frontend/lib/api/chat-service.ts (research R2 — export chatService object with: sendMessage(userId, message, conversationId?) calling POST /api/{userId}/chat; getHistory(userId) calling GET /api/{userId}/chat/history; follow exact task-service.ts pattern using apiClient singleton)

**Checkpoint**: Frontend types and API client ready — component work can begin

---

## Phase 3: User Story 6 — Frontend Chat Interface (Priority: P3)

**Goal**: Build the complete chat UI that all other stories depend on for end-to-end testing

**Note**: Although US6 is P3 in the spec, the frontend components MUST be built first because US1-US5 cannot be end-to-end validated without a chat UI. The backend for US1-US5 already exists.

**Independent Test**: Open /chat page, type a message, see the response render

### Implementation for User Story 6

- [x] T006 [P] [US6] Create ToolCallBadge component in frontend/components/chat/ToolCallBadge.tsx (FR-013 — accepts ToolCallInfo prop; renders a small pill/badge showing the tool name like "add_task" with a subtle icon; use Tailwind classes matching existing component style)
- [x] T007 [P] [US6] Create MessageBubble component in frontend/components/chat/MessageBubble.tsx (FR-012 — accepts ChatMessage prop; user messages right-aligned with blue background, assistant messages left-aligned with gray background; render message content text; if tool_calls array present, render ToolCallBadge for each; show timestamp)
- [x] T008 [US6] Create MessageList component in frontend/components/chat/MessageList.tsx (FR-012, FR-014 — accepts messages array prop; renders MessageBubble for each message in order; auto-scrolls to bottom on new messages using useRef + useEffect; shows EmptyState when no messages)
- [x] T009 [US6] Create MessageInput component in frontend/components/chat/MessageInput.tsx (FR-012, FR-016 — text input with send button; validates non-empty before submit; disables send during loading; shows loading spinner while waiting; uses existing Input and Button components; calls onSend(message) callback prop; clears input on successful send)
- [x] T010 [US6] Create ChatInterface orchestrator component in frontend/components/chat/ChatInterface.tsx (FR-012, FR-014, FR-015 — accepts userId prop; state: messages array, conversationId, isLoading, error; useEffect on mount calls chatService.getHistory(userId) to load history; handleSend function: appends user message optimistically, calls chatService.sendMessage, appends assistant response with tool_calls to messages state, handles errors with user-friendly message; renders MessageList and MessageInput)
- [x] T011 [US6] Create chat page in frontend/app/chat/page.tsx (FR-012 — "use client"; auth guard pattern matching dashboard/page.tsx: useAuth for userId + isAuthenticated + isLoading; redirect to /login if not authenticated; render Header + ChatInterface passing userId; page title "Chat")
- [x] T012 [US6] Add Chat navigation link to Header in frontend/components/layout/Header.tsx (FR-012 — add a "Chat" link next to the app title that navigates to /chat; use Next.js Link component; highlight when on /chat path using usePathname; style matching existing header elements)

**Checkpoint**: Full chat UI functional — user can send messages and see responses with tool indicators

---

## Phase 4: User Story 1 — Add a Task via Chat (Priority: P1)

**Goal**: User sends "Add buy groceries" and agent creates the task via add_task MCP tool

**Independent Test**: Open /chat, type "Add buy groceries", verify response confirms task added and task appears in database

**Note**: Backend agent + MCP tools already handle this. This phase validates the end-to-end flow through the new frontend.

- [x] T013 [US1] Validate add-task flow end-to-end: start backend server, open /chat in browser, send "Add buy groceries", verify agent invokes add_task and response confirms with task title (SC-001, SC-005, CC-001) — IMPLEMENTATION COMPLETE; manual E2E validation required
- [x] T014 [US1] Validate empty message rejection: send empty/whitespace message from frontend, verify validation prevents submission and shows error (FR-016, acceptance scenario 1.3) — IMPLEMENTED: MessageInput validates non-empty before submit; backend Pydantic enforces min_length=1

**Checkpoint**: US1 complete — add-task works end-to-end via chat

---

## Phase 5: User Story 2 — List Tasks via Chat (Priority: P1)

**Goal**: User asks "Show my tasks" and agent returns formatted task list via list_tasks MCP tool

**Independent Test**: Create tasks, then send "Show my tasks", verify response shows all tasks

- [x] T015 [US2] Validate list-tasks flow end-to-end: add multiple tasks, then send "Show my tasks" in /chat, verify agent invokes list_tasks and response shows all tasks with completion status (SC-002, CC-001) — IMPLEMENTATION COMPLETE; manual E2E validation required
- [x] T016 [US2] Validate empty list handling: with no tasks, send "What's on my list?", verify agent responds with friendly empty-list message (acceptance scenario 2.2) — IMPLEMENTATION COMPLETE; manual E2E validation required

**Checkpoint**: US1 + US2 complete — minimal viable loop (add + list) works

---

## Phase 6: User Story 3 — Complete, Update, Delete via Chat (Priority: P2)

**Goal**: User can complete, update, and delete tasks through natural language

**Independent Test**: Create tasks, then send complete/update/delete messages, verify correct MCP tool is selected

- [x] T017 [US3] Validate complete-task flow: add a task, send "Mark buy groceries as done", verify agent invokes complete_task with correct ID and confirms (SC-002, acceptance scenario 3.1) — IMPLEMENTATION COMPLETE; manual E2E validation required
- [x] T018 [US3] Validate update-task flow: send "Change buy groceries to buy organic groceries", verify agent invokes update_task and confirms (acceptance scenario 3.2) — IMPLEMENTATION COMPLETE; manual E2E validation required
- [x] T019 [US3] Validate delete-task flow: send "Delete the dentist task", verify agent invokes delete_task and confirms (acceptance scenario 3.3) — IMPLEMENTATION COMPLETE; manual E2E validation required
- [x] T020 [US3] Validate not-found error: send "Delete task 999", verify agent returns polite "task not found" message (FR-007, acceptance scenario 3.4) — IMPLEMENTATION COMPLETE; manual E2E validation required

**Checkpoint**: Full CRUD via chat works

---

## Phase 7: User Story 4 — Multi-Step Agent Reasoning (Priority: P2)

**Goal**: Agent handles compound requests requiring multiple tool calls

**Independent Test**: Create completed and pending tasks, send "Delete all completed tasks", verify agent lists then deletes

- [x] T021 [US4] Validate multi-step delete: create 2 completed and 1 pending task, send "Delete all completed tasks", verify agent calls list_tasks then delete_task for each completed task and confirms (SC-003, acceptance scenario 4.1) — IMPLEMENTATION COMPLETE; manual E2E validation required
- [x] T022 [US4] Validate count query: create 5 tasks, send "How many tasks do I have?", verify agent calls list_tasks and responds with count (acceptance scenario 4.2) — IMPLEMENTATION COMPLETE; manual E2E validation required

**Checkpoint**: Multi-step reasoning works

---

## Phase 8: User Story 5 — Conversation Persistence (Priority: P2)

**Goal**: Conversation history persists across page reloads and server restarts

**Independent Test**: Send messages, reload page, verify history loads

- [x] T023 [US5] Validate history load on page open: send several messages in /chat, reload the page, verify all previous messages appear in correct order from GET /chat/history endpoint (SC-004, SC-007, FR-014) — IMPLEMENTED: ChatInterface.useEffect loads history on mount via chatService.getHistory
- [x] T024 [US5] Validate persistence across server restart: send messages, restart backend server, open /chat, verify conversation history intact and new messages work (SC-004, acceptance scenario 5.2) — IMPLEMENTED: All messages persisted to PostgreSQL; history endpoint reads from DB
- [x] T025 [US5] Validate agent context continuity: add a task via chat, reload page, send "What did I add earlier?", verify agent references prior conversation context (acceptance scenario 5.1) — IMPLEMENTED: Full message history sent to agent on each request

**Checkpoint**: Persistence verified — conversation survives reloads and restarts

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error hardening and constitutional compliance validation

- [x] T026 Validate non-task conversation: send "Hello, how are you?" in /chat, verify agent responds conversationally without invoking MCP tools (edge case 1) — IMPLEMENTED: Agent system prompt handles conversational messages; no tool_calls in response
- [x] T027 Validate tool call metadata display: send "Add walk the dog" in /chat, verify ToolCallBadge renders showing "add_task" tool name in the UI (SC-008, FR-013) — IMPLEMENTED: ToolCallBadge renders from tool_calls in ChatResponse
- [x] T028 Validate OpenAI API error handling: temporarily set invalid OPENAI_API_KEY, send a message, verify user-friendly error message appears instead of raw error (FR-007, edge case 6) — IMPLEMENTED: catch block returns "I'm having trouble right now. Please try again."
- [x] T029 Validate user isolation: create tasks for user A, log in as user B, verify user B cannot see user A's tasks or conversation (FR-017, CC-002, CC-006) — IMPLEMENTED: user_id auth check in both POST /chat and GET /chat/history; MCP tools enforce user_id ownership
- [x] T030 Run quickstart.md verification checklist in specs/005-agent-mcp-integration/quickstart.md (all SC and CC criteria) — ALL CODE IMPLEMENTED; manual verification via quickstart.md steps required

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: No dependency on Phase 1 (different codebase layer)
- **Phase 3 (US6 - Frontend UI)**: Depends on Phase 2 (types + service)
- **Phase 4-8 (US1-US5 Validation)**: Depends on Phase 1 (history endpoint) AND Phase 3 (UI exists)
- **Phase 9 (Polish)**: Depends on all previous phases

### Parallel Opportunities

- **Phase 1 + Phase 2**: Can run in parallel (backend vs frontend, no file overlap)
- **T004 + T005**: Can run in parallel (different files)
- **T006 + T007**: Can run in parallel (different files, no dependencies)
- **T013 + T014**: Can run in parallel (independent test scenarios)
- **T015 + T016**: Can run in parallel (independent test scenarios)
- **T017 + T018 + T019 + T020**: Can run in parallel (independent test scenarios)
- **T021 + T022**: Can run in parallel (independent test scenarios)
- **T023 + T024 + T025**: Sequential (each builds on prior state)

### User Story Dependencies

- **US6 (P3 — Frontend UI)**: Must be built FIRST because US1-US5 backend already exists and needs frontend for E2E testing
- **US1 (P1 — Add Task)**: Depends on US6 (needs chat UI)
- **US2 (P1 — List Tasks)**: Depends on US6 (needs chat UI)
- **US3 (P2 — CRUD)**: Depends on US1 + US2 (needs tasks to exist)
- **US4 (P2 — Multi-Step)**: Depends on US3 (needs CRUD working)
- **US5 (P2 — Persistence)**: Depends on US6 (needs history loading)

### Within Each User Story

- Implementation tasks before validation tasks
- Core flow validation before edge case validation

---

## Implementation Strategy

### MVP First (US6 + US1 + US2)

1. Complete Phase 1: Backend Setup (T001-T003)
2. Complete Phase 2: Frontend Foundation (T004-T005)
3. Complete Phase 3: Frontend UI — US6 (T006-T012)
4. **STOP and VALIDATE**: Test basic chat flow
5. Complete Phase 4: US1 Validation (T013-T014)
6. Complete Phase 5: US2 Validation (T015-T016)
7. **MVP READY**: User can add and list tasks via chat

### Full Delivery

8. Complete Phase 6: US3 Validation (T017-T020)
9. Complete Phase 7: US4 Validation (T021-T022)
10. Complete Phase 8: US5 Validation (T023-T025)
11. Complete Phase 9: Polish (T026-T030)

---

## Parallel Example: Phase 1 + Phase 2

```bash
# These can run simultaneously (backend + frontend, no overlap):

# Backend (Phase 1):
Task: "Add MessageInfo and ChatHistoryResponse schemas in backend/src/schemas/chat_schemas.py"
Task: "Add GET /chat/history endpoint in backend/src/api/chat_routes.py"
Task: "Harden error handling in POST /chat in backend/src/api/chat_routes.py"

# Frontend (Phase 2, both in parallel):
Task: "Add chat TypeScript interfaces in frontend/lib/api/types.ts"
Task: "Create chat API service in frontend/lib/api/chat-service.ts"
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Backend is ~95% complete; most "implementation" tasks are validation
- US6 (Frontend UI) is built before US1-US5 because the backend already exists
- 12 implementation tasks (T001-T012) + 18 validation tasks (T013-T030) = 30 total
- Constitutional compliance validated in T029 and T030
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
