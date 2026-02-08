# Feature Specification: Phase III - Todo AI Chatbot

**Feature Branch**: `004-todo-ai-chatbot`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Phase III: Todo AI Chatbot (Master Specification) — AI-powered Todo chatbot that manages tasks via natural language using OpenAI Agents SDK and MCP, with agent backend integrated with ChatKit frontend, stateless backend, persistent conversations in PostgreSQL."

## Purpose

Build an AI-powered Todo chatbot that manages tasks via natural language
using OpenAI Agents SDK and MCP (Model Context Protocol), with the agent
backend fully integrated with the frontend chat UI, while maintaining a
stateless backend and persistent conversations in PostgreSQL.

## Scope

**In scope:**

- Conversational task management (add, list, update, complete, delete)
- Agent-driven reasoning via OpenAI Agents SDK
- MCP-based tool invocation (5 tools)
- Stateless chat API with durable conversation memory
- End-to-end integration between ChatKit frontend and agent backend
- Conversation persistence and reconstruction across restarts
- Multi-user isolation at the MCP tool layer
- Graceful error handling surfaced in the chat UI

**Out of scope:**

- Advanced analytics or reporting dashboards
- Push notifications or real-time alerts
- Manual task editing outside the chat interface
- Multi-agent orchestration
- Voice input or multimedia messages
- Task sharing or collaboration between users
- Scheduled or recurring tasks

## System Principles (Hard Constraints)

- Backend servers MUST be stateless
- PostgreSQL MUST be the single source of truth
- AI agents MUST NOT access the database directly
- All task mutations MUST occur via MCP tools only
- Conversation state MUST be reconstructed per request
- Frontend MUST NOT call MCP or database directly
- Frontend MUST communicate only with the agent backend via chat API

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a Task via Chat (Priority: P1)

A user opens the chat interface and types a natural language request
like "Add a task to buy groceries." The system interprets the intent,
creates the task using the appropriate tool, and confirms the creation
in the chat with the task details.

**Why this priority**: Task creation is the foundational action. Without
it, no other task management is possible. This proves the full pipeline
works end-to-end: user message → agent reasoning → MCP tool → database
→ confirmation response.

**Independent Test**: Can be fully tested by sending a chat message with
a task creation request and verifying the task appears in the database
and the agent responds with a confirmation.

**Acceptance Scenarios**:

1. **Given** a user with no existing tasks, **When** the user sends
   "Add a task to buy groceries", **Then** the system creates a task
   with title "buy groceries" and responds with a confirmation message
   including the task title.
2. **Given** a user sends "Add task: finish project report by Friday",
   **When** the agent processes the message, **Then** a task is created
   with the provided title and the agent confirms with the task details.
3. **Given** a user sends a vague message like "remember milk", **When**
   the agent processes it, **Then** the agent interprets the intent as
   task creation and creates a task with an appropriate title.

---

### User Story 2 - List Tasks via Chat (Priority: P1)

A user asks to see their tasks by typing something like "Show me my
tasks" or "What's on my list?" The agent retrieves the user's tasks
and presents them in a readable format within the chat.

**Why this priority**: Listing tasks is co-equal with creation — users
need to see what they have before they can manage it. This validates
the read path through MCP tools.

**Independent Test**: Can be tested by first adding tasks, then sending
a list request and verifying the response contains all existing tasks.

**Acceptance Scenarios**:

1. **Given** a user with 3 existing tasks, **When** the user sends
   "Show my tasks", **Then** the agent responds with all 3 tasks in
   a readable format.
2. **Given** a user with no tasks, **When** the user sends "List my
   tasks", **Then** the agent responds indicating no tasks exist.
3. **Given** a user with both completed and incomplete tasks, **When**
   the user sends "What do I need to do?", **Then** the agent lists
   the tasks with completion status indicated.

---

### User Story 3 - Complete a Task via Chat (Priority: P2)

A user tells the chatbot they've finished a task, e.g., "I finished
buying groceries" or "Mark task 1 as done." The agent identifies the
task and marks it as completed.

**Why this priority**: Completing tasks is the core value loop — users
add tasks to track them and complete them when done. This requires
the agent to resolve task references (by name or ID).

**Independent Test**: Can be tested by adding a task, then sending a
completion message and verifying the task's completed status changes.

**Acceptance Scenarios**:

1. **Given** a user has a task titled "buy groceries", **When** the
   user sends "I finished buying groceries", **Then** the agent marks
   that task as completed and confirms.
2. **Given** a user references a task that does not exist, **When**
   the user sends "Complete task 999", **Then** the agent responds
   with a friendly error indicating the task was not found.
3. **Given** a user has multiple tasks with similar names, **When**
   the user sends an ambiguous completion request, **Then** the agent
   lists matching tasks and asks for clarification.

---

### User Story 4 - Update a Task via Chat (Priority: P2)

A user wants to modify an existing task, e.g., "Change 'buy groceries'
to 'buy groceries and cleaning supplies'" or "Update task 2 description
to include the deadline." The agent finds the task and updates it.

**Why this priority**: Updating enables correction and refinement of
tasks without deletion and recreation. Validates the update MCP tool.

**Independent Test**: Can be tested by adding a task, sending an
update request, and verifying the task's title or description changed.

**Acceptance Scenarios**:

1. **Given** a user has a task titled "buy groceries", **When** the
   user sends "Change it to buy groceries and snacks", **Then** the
   agent updates the task title and confirms the change.
2. **Given** a user references a non-existent task for update, **When**
   the agent processes the request, **Then** it responds with an error
   indicating the task was not found.

---

### User Story 5 - Delete a Task via Chat (Priority: P2)

A user requests deletion of a task, e.g., "Delete the groceries task"
or "Remove task 3." The agent identifies and deletes the task.

**Why this priority**: Deletion completes the full CRUD lifecycle.
This may require multi-step reasoning (list then delete).

**Independent Test**: Can be tested by adding a task, sending a
delete request, and verifying the task no longer exists.

**Acceptance Scenarios**:

1. **Given** a user has a task titled "buy groceries", **When** the
   user sends "Delete the groceries task", **Then** the agent deletes
   the task and confirms deletion.
2. **Given** a user sends "Delete all completed tasks", **When** the
   agent processes the request, **Then** it lists completed tasks,
   deletes each one, and confirms the bulk operation.
3. **Given** a user references a task that does not exist, **When**
   the agent processes the delete request, **Then** it responds with
   a friendly error that the task was not found.

---

### User Story 6 - Conversation Persistence (Priority: P3)

A user has an ongoing conversation, the server restarts, and the user
sends a new message. The system reconstructs the conversation history
from the database and the agent continues seamlessly.

**Why this priority**: Persistence proves the stateless architecture
works correctly. Without it, conversations break on every restart.

**Independent Test**: Can be tested by sending messages, simulating
a restart (new request with same conversation_id), and verifying the
agent references prior conversation context.

**Acceptance Scenarios**:

1. **Given** a user has an existing conversation with 5 messages,
   **When** a new request arrives on a fresh server instance, **Then**
   the conversation history is loaded from the database and the agent
   responds with full context awareness.
2. **Given** a new user with no prior conversation, **When** they
   send their first message, **Then** a new conversation is created
   and the agent responds appropriately.

---

### User Story 7 - Multi-Step Agent Reasoning (Priority: P3)

A user makes a complex request that requires the agent to chain
multiple MCP tool calls, e.g., "Delete all my completed tasks" requires
listing tasks first, filtering completed ones, then deleting each.

**Why this priority**: This validates the agent's reasoning capability
beyond single-tool invocations. It proves the OpenAI Agents SDK
integration supports sequential tool use.

**Independent Test**: Can be tested by creating several tasks (some
completed), sending a multi-step request, and verifying all expected
operations were performed.

**Acceptance Scenarios**:

1. **Given** a user has 3 completed and 2 incomplete tasks, **When**
   the user sends "Delete all completed tasks", **Then** the agent
   lists tasks, identifies the 3 completed ones, deletes each, and
   confirms the operation.
2. **Given** a user sends "How many tasks do I have left?", **When**
   the agent processes the request, **Then** it lists tasks and counts
   the incomplete ones, responding with the count.

---

### Edge Cases

- What happens when the user sends an empty message?
  The system MUST return a friendly prompt asking the user to type a request.
- What happens when the user sends a message that has no task-related intent?
  The agent MUST respond conversationally without invoking any MCP tool.
- What happens when the database is unreachable?
  The system MUST return an explicit error message and not crash silently.
- What happens when the user sends extremely long messages (>10,000 characters)?
  The system MUST handle gracefully, either processing or returning a
  length validation error.
- What happens when two requests for the same user arrive simultaneously?
  The system MUST handle concurrent requests without data corruption,
  relying on database-level consistency.
- What happens when the MCP tool returns an unexpected error?
  The agent MUST surface a user-friendly error message without exposing
  internal details.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept natural language messages via a chat
  endpoint and return agent-generated responses.
- **FR-002**: System MUST create tasks when the user expresses intent
  to add a task, using the `add_task` MCP tool.
- **FR-003**: System MUST list a user's tasks when requested, using
  the `list_tasks` MCP tool.
- **FR-004**: System MUST mark tasks as completed when the user
  indicates completion, using the `complete_task` MCP tool.
- **FR-005**: System MUST update task details when the user requests
  changes, using the `update_task` MCP tool.
- **FR-006**: System MUST delete tasks when the user requests removal,
  using the `delete_task` MCP tool.
- **FR-007**: System MUST persist all conversation messages (user and
  assistant) to the database after each request.
- **FR-008**: System MUST reconstruct conversation history from the
  database at the start of each request.
- **FR-009**: System MUST create a new conversation automatically
  when no conversation_id is provided.
- **FR-010**: System MUST enforce user ownership — a user can only
  access and modify their own tasks and conversations.
- **FR-011**: System MUST support multi-step agent reasoning where a
  single user request triggers multiple MCP tool calls.
- **FR-012**: System MUST return structured responses including the
  conversation_id, the agent's response text, and optionally the
  tool calls made.
- **FR-013**: System MUST handle errors gracefully — missing tasks,
  invalid IDs, empty task lists, and database failures MUST produce
  user-friendly error messages.
- **FR-014**: The AI agent MUST NOT fabricate task IDs, user data,
  or tool outputs under any circumstances.
- **FR-015**: The frontend MUST render agent responses in a chat
  interface and send user messages to the backend chat endpoint.
- **FR-016**: The frontend MUST NOT contain business logic, MCP calls,
  or direct database access.
- **FR-017**: System MUST authenticate users via Better Auth before
  allowing access to the chat endpoint.

### Key Entities

- **Task**: Represents a single todo item belonging to a user.
  Key attributes: unique identifier, owner (user), title, description,
  completion status, creation timestamp, last update timestamp.
- **Conversation**: Represents a chat session for a user. Key
  attributes: unique identifier, owner (user), creation timestamp,
  last update timestamp.
- **Message**: Represents a single message in a conversation. Key
  attributes: unique identifier, parent conversation, sender (user),
  role (user or assistant), content text, creation timestamp.

## Assumptions

- Each user has at most one active conversation at a time (new
  conversations are created on first message if none exists).
- Task titles are the primary identifier for natural language
  references; the agent resolves names to IDs internally.
- The OpenAI Agents SDK handles tool selection and multi-step
  reasoning without additional custom orchestration logic.
- Better Auth is already available from Phase II and provides
  user identity for the `user_id` path parameter.
- The ChatKit frontend is a pre-built component that requires
  minimal configuration to connect to the backend endpoint.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task via chat in under 5 seconds
  from message send to confirmation response.
- **SC-002**: Users can view their complete task list via a single
  chat message.
- **SC-003**: Multi-step operations (e.g., "delete all completed
  tasks") complete successfully in a single user request.
- **SC-004**: Conversation history persists across server restarts
  with zero message loss.
- **SC-005**: 100% of task mutations occur exclusively through MCP
  tools — no direct database writes from the agent.
- **SC-006**: Each user's tasks are completely isolated; no user
  can view or modify another user's data.
- **SC-007**: The agent responds appropriately to non-task messages
  without invoking MCP tools.

### Constitutional Compliance Outcomes

- **CC-001**: End-to-end flow works: user sends chat message, agent
  selects correct MCP tool, tool executes, agent responds in natural
  language.
- **CC-002**: Each user can only see and modify their own tasks via
  MCP tools.
- **CC-003**: MCP tools validate all inputs and enforce user ownership.
- **CC-004**: All specs pass implementation review without deviation
  from approved specification.
- **CC-005**: FastAPI server remains stateless; all state persisted
  in PostgreSQL.
- **CC-006**: Cross-user data access is impossible due to MCP-layer
  isolation.
- **CC-007**: Conversation state reconstructed from database on every
  request.
- **CC-008**: AI agent never hallucinated task IDs or fabricates tool
  outputs.
- **CC-009**: Only approved MCP tools used (add_task, list_tasks,
  complete_task, update_task, delete_task).
