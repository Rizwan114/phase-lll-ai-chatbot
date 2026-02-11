# Feature Specification: AI Agent, MCP Orchestration & Frontend Integration

**Feature Branch**: `005-agent-mcp-integration`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Spec-4: AI Agent, MCP Orchestration & Frontend Integration"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a Task via Chat (Priority: P1)

A user opens the chat interface in the frontend, types a natural language
message like "Add buy groceries to my list", and receives a confirmation
from the assistant that the task was created. The assistant mentions the
task title in its response.

**Why this priority**: Adding tasks is the most fundamental action. If the
agent cannot interpret an "add" intent and invoke the correct MCP tool,
no other functionality works. This is the MVP slice.

**Independent Test**: Send a chat message with an add-intent phrase.
Verify the assistant response confirms the task was added and the task
appears in the database for that user.

**Acceptance Scenarios**:

1. **Given** a user with an active conversation, **When** the user sends
   "Add buy groceries", **Then** the agent invokes `add_task` with the
   correct title and returns a friendly confirmation mentioning
   "buy groceries".
2. **Given** a user with an active conversation, **When** the user sends
   "Remember to call the dentist tomorrow", **Then** the agent invokes
   `add_task` with the title "call the dentist tomorrow" and confirms.
3. **Given** a user with an active conversation, **When** the user sends
   an empty or whitespace-only message, **Then** the system returns a
   validation error without invoking the agent.

---

### User Story 2 - List Tasks via Chat (Priority: P1)

A user asks the assistant "What's on my list?" or "Show my tasks" and
receives a formatted list of their current tasks, including completion
status.

**Why this priority**: Listing is the read complement to adding. Together
with US1, it forms the minimal viable loop (add + view).

**Independent Test**: Create tasks for a user, then send a list-intent
message. Verify the response contains all tasks with their statuses.

**Acceptance Scenarios**:

1. **Given** a user with 3 tasks (2 pending, 1 completed), **When** the
   user sends "Show my tasks", **Then** the agent invokes `list_tasks`
   and returns all 3 tasks with their completion status.
2. **Given** a user with no tasks, **When** the user sends "What's on my
   list?", **Then** the agent invokes `list_tasks` and responds with a
   friendly message indicating the list is empty.

---

### User Story 3 - Complete, Update, and Delete Tasks via Chat (Priority: P2)

A user can mark tasks as complete ("Mark buy groceries as done"), update
task details ("Change buy groceries to buy organic groceries"), or delete
tasks ("Delete the dentist task") through natural language. The agent
identifies the correct task and invokes the appropriate MCP tool.

**Why this priority**: Mutation operations complete the full CRUD cycle.
They depend on the add/list foundation from US1 and US2 but are essential
for a usable product.

**Independent Test**: Create tasks, then send complete/update/delete
messages. Verify the agent selects the correct MCP tool, targets the
right task, and confirms the action.

**Acceptance Scenarios**:

1. **Given** a user with a task "buy groceries" (id=1, pending), **When**
   the user sends "Mark buy groceries as done", **Then** the agent invokes
   `complete_task` with the correct task ID and confirms completion.
2. **Given** a user with a task "buy groceries", **When** the user sends
   "Change buy groceries to buy organic groceries", **Then** the agent
   invokes `update_task` with the new title and confirms the update.
3. **Given** a user with a task "call dentist", **When** the user sends
   "Delete the dentist task", **Then** the agent invokes `delete_task`
   with the correct task ID and confirms deletion.
4. **Given** a user who says "Delete task 999" (non-existent), **When**
   the agent attempts the operation, **Then** the agent returns a polite
   message that the task was not found.

---

### User Story 4 - Multi-Step Agent Reasoning (Priority: P2)

A user issues a compound request like "Delete all completed tasks" or
"How many tasks do I have left?". The agent performs multi-step reasoning:
first listing tasks to gather context, then performing the appropriate
follow-up actions.

**Why this priority**: Multi-step reasoning differentiates an intelligent
agent from a simple command mapper. It is required for natural
conversational interaction.

**Independent Test**: Create a mix of completed and pending tasks. Send
"Delete all completed tasks". Verify the agent lists tasks first, then
deletes only the completed ones, and confirms each deletion.

**Acceptance Scenarios**:

1. **Given** a user with 2 completed and 1 pending task, **When** the user
   sends "Delete all completed tasks", **Then** the agent calls
   `list_tasks`, identifies the 2 completed tasks, calls `delete_task`
   for each, and confirms both deletions.
2. **Given** a user with 5 tasks, **When** the user sends "How many tasks
   do I have?", **Then** the agent calls `list_tasks` and responds with
   the count.

---

### User Story 5 - Conversation Persistence (Priority: P2)

A user chats with the assistant, closes the browser, returns later, and
the conversation history is intact. The agent remembers prior context
within the same conversation.

**Why this priority**: Persistence is a constitutional requirement.
Without it, every page reload loses context, making the chatbot unusable
for real workflows.

**Independent Test**: Send messages, restart the server or reload the
page, then send a follow-up message. Verify the agent has access to the
full conversation history.

**Acceptance Scenarios**:

1. **Given** a user who previously said "Add buy groceries", **When** the
   user returns and asks "What did I add earlier?", **Then** the agent
   reconstructs the conversation from the database and references the
   prior task.
2. **Given** a server restart between messages, **When** the user sends a
   new message, **Then** the conversation continues seamlessly with full
   history available.

---

### User Story 6 - Frontend Chat Interface (Priority: P3)

The frontend provides a dedicated chat page where users can type messages,
see assistant responses, and observe tool activity indicators. The chat
interface integrates with the backend chat endpoint.

**Why this priority**: The frontend is the user-facing layer. While the
backend can be tested via API, the frontend delivers the actual user
experience. It depends on all backend stories being functional.

**Independent Test**: Open the chat page, type a message, and verify the
assistant response renders correctly. Verify tool call metadata is
displayed when available.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the chat page, **When** the user
   types "Add walk the dog" and submits, **Then** the message appears in
   the chat, and the assistant's confirmation response renders below it.
2. **Given** an assistant response that includes tool call metadata,
   **When** the response renders, **Then** the UI displays a tool
   activity indicator showing which MCP tool was invoked.
3. **Given** a user who navigates away and returns to the chat page,
   **When** the page loads, **Then** previous messages are loaded from
   the backend and displayed in order.

---

### Edge Cases

- What happens when the user sends a message that does not map to any
  task action (e.g., "What's the weather?")?
  The agent responds conversationally without invoking any MCP tool.
- What happens when the agent cannot determine which task the user means
  (ambiguous reference)?
  The agent asks a clarifying question (e.g., "Which task did you mean:
  'buy groceries' or 'buy milk'?").
- What happens when the MCP tool subprocess fails to start?
  The system returns an explicit error message to the user and logs the
  failure for debugging.
- What happens when the user sends an extremely long message (>5000
  characters)?
  The system rejects the message with a validation error before reaching
  the agent.
- What happens when concurrent requests arrive for the same user?
  Each request independently reconstructs conversation state from the
  database; the last-write-wins for message ordering.
- What happens when the OpenAI API is unreachable or returns an error?
  The system returns a user-friendly error ("I'm having trouble thinking
  right now. Please try again.") and logs the API error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept user messages via
  `POST /api/{user_id}/chat` and return an assistant response.
- **FR-002**: The AI agent MUST interpret natural language input and
  select the correct MCP tool based on user intent.
- **FR-003**: The agent MUST use only the 5 approved MCP tools for task
  mutations: `add_task`, `list_tasks`, `complete_task`, `update_task`,
  `delete_task`.
- **FR-004**: The agent MUST NOT access the database directly; all data
  operations MUST go through MCP tools.
- **FR-005**: The agent MUST NOT assume or fabricate task IDs; it MUST
  discover them via `list_tasks` when needed.
- **FR-006**: The agent MUST confirm successful mutations by mentioning
  the task title and keeping responses short and friendly.
- **FR-007**: The agent MUST handle errors gracefully: missing tasks
  produce polite messages, ambiguous input triggers clarification,
  tool failures produce user-friendly fallback responses.
- **FR-008**: The agent MUST perform multi-step reasoning when required
  (e.g., list then delete for "delete all completed tasks").
- **FR-009**: Every user message and assistant response MUST be persisted
  to the database as part of the conversation.
- **FR-010**: Conversation state MUST be reconstructed from the database
  on every request; no in-memory chat state is permitted.
- **FR-011**: The chat endpoint response MUST include: assistant response
  text, conversation ID, and MCP tool call metadata (tool name,
  arguments, result summary).
- **FR-012**: The frontend MUST provide a chat page where users send
  messages and view assistant responses.
- **FR-013**: The frontend MUST render tool activity indicators when the
  response includes MCP tool call metadata.
- **FR-014**: The frontend MUST load and display conversation history
  when the chat page is opened.
- **FR-015**: The frontend MUST send messages to the backend chat
  endpoint using the authenticated user's ID and session token.
- **FR-016**: The system MUST validate message input: reject empty
  messages, enforce a maximum length, and return clear error messages.
- **FR-017**: The system MUST enforce user isolation: each user can only
  interact with their own tasks and conversation history.

### Intent-to-Tool Mapping

The agent MUST follow this mapping when interpreting user intent:

| User Intent Pattern          | MCP Tool        |
| ---------------------------- | --------------- |
| Add / remember / create      | `add_task`      |
| List / show / what's on      | `list_tasks`    |
| Complete / done / finish     | `complete_task` |
| Delete / remove / get rid of | `delete_task`   |
| Update / change / rename     | `update_task`   |

### Key Entities

- **Conversation**: A persistent chat session belonging to a single user.
  One active conversation per user. Contains an ordered sequence of
  messages.
- **Message**: A single utterance in a conversation. Has a role (user or
  assistant), content text, and timestamp. Messages are ordered
  chronologically within a conversation.
- **Task**: A user's todo item managed exclusively through MCP tools.
  Has a title, optional description, completion status, and user
  ownership.
- **Tool Call**: Metadata describing an MCP tool invocation: tool name,
  arguments passed, and result summary. Returned to the frontend for
  display but not persisted as a separate entity.

## Assumptions

- Authentication (JWT via Better Auth) is already implemented and
  functional from Phase II. This spec does not redefine auth.
- Database schema for Conversation and Message models already exists
  from prior implementation work.
- MCP tools (all 5) are already implemented and functional in
  `backend/src/mcp/server.py`.
- The agent configuration and runner are already implemented in
  `backend/src/agent/`.
- The chat endpoint `POST /api/{user_id}/chat` is already implemented
  in `backend/src/api/chat_routes.py`.
- The frontend uses Next.js with App Router and has existing auth pages
  and a dashboard page.

## Scope Boundaries

**In scope**:
- Agent behavior, intent detection, and MCP tool selection
- MCP tool orchestration and multi-step reasoning
- Backend chat endpoint response contract (tool call metadata)
- Frontend chat page, message rendering, and tool activity indicators
- Frontend chat API client integration
- Conversation history loading and display
- Error handling and edge cases for agent interactions
- Input validation for chat messages

**Out of scope**:
- UI visual design and styling decisions
- Database schema changes (models already exist)
- Authentication implementation (already complete)
- MCP tool internals (already implemented)
- Agent system prompt tuning beyond functional correctness
- Real-time streaming (future enhancement; current approach returns
  complete responses)
- Notification systems
- Task sharing between users

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task via chat and receive confirmation
  within 5 seconds of sending the message.
- **SC-002**: Users can list, complete, update, and delete tasks via
  natural language with 100% correct tool selection for unambiguous
  intents.
- **SC-003**: Multi-step operations (e.g., "delete all completed tasks")
  complete successfully with correct task targeting.
- **SC-004**: Conversation history survives page reloads and server
  restarts with zero message loss.
- **SC-005**: 100% of task mutations produce a confirmation response
  that mentions the affected task by title.
- **SC-006**: Error scenarios (missing task, tool failure, API
  unreachable) produce user-friendly messages instead of raw errors.
- **SC-007**: The frontend chat page loads conversation history and
  renders messages in correct chronological order.
- **SC-008**: Tool activity indicators display in the frontend when
  MCP tools are invoked.

### Constitutional Compliance Outcomes

- **CC-001**: End-to-end flow works: user sends chat message, agent
  selects correct MCP tool, tool executes, agent responds in natural
  language.
- **CC-002**: Each user can only see and modify their own tasks via
  MCP tools.
- **CC-003**: MCP tools validate all inputs and enforce user ownership.
- **CC-004**: All implementation traces back to this approved
  specification without deviation.
- **CC-005**: The server remains stateless; all state persisted in
  the database.
- **CC-006**: Cross-user data access is impossible due to MCP-layer
  isolation.
- **CC-007**: Conversation state is reconstructed from the database
  on every request.
- **CC-008**: The AI agent never hallucinates task IDs or fabricates
  tool outputs.
- **CC-009**: Only approved MCP tools are used (add_task, list_tasks,
  complete_task, update_task, delete_task).
