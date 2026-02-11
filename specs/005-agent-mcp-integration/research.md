# Research: AI Agent, MCP Orchestration & Frontend Integration

**Branch**: `005-agent-mcp-integration` | **Date**: 2026-02-11

## R1: Existing Backend Implementation Status

**Decision**: The backend is fully implemented and requires validation, not
re-implementation.

**Findings**:
- Agent (`backend/src/agent/agent.py`): Uses `gpt-4o-mini` model with
  comprehensive system prompt covering all 5 MCP tools, user_id
  injection rules, multi-step reasoning, error handling, and
  anti-hallucination constraints.
- Runner (`backend/src/agent/runner.py`): Async function launches MCP
  server as stdio subprocess, augments messages with user_id context,
  extracts tool calls from `raw_responses`, returns `ChatResult`
  dataclass.
- MCP Server (`backend/src/mcp/server.py`): All 5 tools implemented
  with input validation, user ownership enforcement, structured JSON
  returns, and error handling.
- Chat Endpoint (`backend/src/api/chat_routes.py`): 8-step flow —
  auth check, get/create conversation, load history, persist user
  message, run agent, persist response, update timestamp, return
  structured response.
- Schemas (`backend/src/schemas/chat_schemas.py`): `ChatRequest`
  (message + optional conversation_id), `ChatResponse`
  (conversation_id + response + optional tool_calls),
  `ToolCallInfo` (tool + input + output).

**Rationale**: No unknowns or NEEDS CLARIFICATION in the backend.
All spec requirements (FR-001 through FR-011, FR-016, FR-017)
are already addressed in code.

**Alternatives Considered**: None. The implementation matches the
spec; re-implementation would violate the smallest-diff principle.

## R2: Frontend Chat Integration Pattern

**Decision**: Create a `chat-service.ts` following the existing
`task-service.ts` pattern, plus new chat components.

**Findings**:
- `apiClient` singleton handles auth headers, 401 redirect, error
  parsing — chat service MUST use this same client.
- `task-service.ts` pattern: export a service object with typed
  async methods wrapping `apiClient.post/get`.
- Auth context (`useAuth`) provides `userId` and `getToken()` —
  chat page MUST use `userId` for the endpoint path.
- Existing UI components: `Button`, `Input`, `Card`, `Spinner`,
  `EmptyState`, `ErrorState` — all reusable in chat UI.
- Next.js App Router: pages in `frontend/app/`, components in
  `frontend/components/`.

**Rationale**: Consistency with existing patterns reduces cognitive
load and leverages the proven apiClient auth flow.

**Alternatives Considered**:
- WebSocket for real-time streaming → Rejected (out of scope per spec;
  current approach returns complete responses).
- Separate fetch logic → Rejected (would bypass apiClient auth
  handling).

## R3: Frontend Chat Page Architecture

**Decision**: New `/chat` page with dedicated components, accessible
from the Header navigation.

**Findings**:
- Dashboard page pattern: auth guard, `useAuth()` for userId,
  Header component, main content area.
- Chat page needs: message list, message input, loading states,
  tool activity indicators.
- Component breakdown:
  - `ChatPage` (`app/chat/page.tsx`) — page wrapper with auth guard
  - `ChatInterface` — orchestrator: manages messages state, sends
    to backend, receives responses
  - `MessageList` — renders message bubbles (user + assistant)
  - `MessageInput` — text input + send button
  - `ToolCallIndicator` — displays MCP tool call metadata

**Rationale**: Follows existing dashboard pattern. Separate components
enable independent testing per US6.

**Alternatives Considered**:
- Embed chat in dashboard → Rejected (dashboard is task-list focused;
  chat is a distinct interaction mode).
- Modal chat widget → Rejected (full page provides better UX for
  conversation history).

## R4: Conversation History Loading

**Decision**: Add a `GET /api/{user_id}/chat/history` endpoint for
loading conversation history on page load.

**Findings**:
- Current `POST /api/{user_id}/chat` sends a message and returns
  the response — it does not return previous messages.
- Frontend needs to load existing messages when chat page opens
  (FR-014).
- Backend has `MessageService.list_by_conversation()` and
  `ConversationService.get_or_create()` ready to support this.
- New endpoint returns the conversation ID and all messages in
  chronological order.

**Rationale**: Separating history retrieval from message sending
follows REST conventions and avoids overloading the POST endpoint.

**Alternatives Considered**:
- Return history in every POST response → Rejected (wasteful for
  every message; grows linearly).
- Client-side message caching → Rejected (violates stateless
  constitution; messages MUST come from DB).

## R5: Message Input Validation

**Decision**: Validate at both frontend and backend layers.

**Findings**:
- Backend already validates via Pydantic: `ChatRequest.message`
  has `min_length=1, max_length=10000`.
- Frontend MUST prevent empty submissions and show character limits
  for UX (FR-016).
- Spec edge case: messages >5000 chars rejected → backend allows
  10000, spec says 5000. Backend's existing 10000 limit is
  acceptable; frontend can show a softer warning at 5000.

**Rationale**: Defense in depth. Frontend validation prevents
unnecessary network calls; backend validation is the trust boundary.

**Alternatives Considered**: Frontend-only validation → Rejected
(violates security-by-design; backend is the authority).

## R6: Error Handling Strategy

**Decision**: Map backend error codes to user-friendly messages
in the chat UI.

**Findings**:
- Backend returns: 401 (token expired/invalid), 403 (wrong user),
  404 (conversation not found), 500 (agent/tool failure).
- `apiClient` already handles 401 → redirect to login.
- Chat-specific errors: agent failure should show
  "I'm having trouble right now. Please try again."
- Tool-specific errors returned in `result.response` by the agent
  itself (e.g., "Task not found").

**Rationale**: Consistent with existing error handling patterns
while providing chat-specific UX.

**Alternatives Considered**: None. This is the standard approach.
