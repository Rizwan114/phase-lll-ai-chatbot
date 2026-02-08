# Research: Phase III - Todo AI Chatbot

**Feature**: 004-todo-ai-chatbot
**Date**: 2026-02-08

## R1: OpenAI Agents SDK

**Decision**: Use `openai-agents` Python package for agent orchestration.

**Rationale**: The OpenAI Agents SDK provides built-in support for MCP
tool integration, conversation management, and multi-step reasoning.
It handles tool selection, execution loops, and response formatting
natively, eliminating the need for custom orchestration logic.

**Key findings**:

- **Package**: `openai-agents` (pip install)
- **Core classes**: `Agent`, `Runner`
- **MCP integration**: `MCPServerStdio` connects to MCP servers via
  stdio transport; tools are auto-discovered from the MCP server
- **Conversation**: Provide message history as a list of dicts
  (`{"role": "user"/"assistant", "content": "..."}`)
- **Execution**: `Runner.run(agent, messages)` returns a `RunResult`
  with `.final_output` (text) and tool call traces
- **Async support**: Full async via `Runner.run()` (awaitable)
- **Multi-step**: SDK automatically loops tool calls until the agent
  produces a final text response

**Alternatives considered**:

| Alternative | Why Rejected |
|---|---|
| LangChain | Heavier, more abstraction layers than needed for 5 tools |
| Custom OpenAI function calling | No MCP integration; manual tool dispatch |
| Anthropic Claude SDK | Constitution specifies OpenAI Agents SDK |

## R2: MCP Server Implementation

**Decision**: Use `mcp` Python package with stdio transport, running
the MCP server as a subprocess managed by the OpenAI Agents SDK.

**Rationale**: Stdio transport is the simplest integration path and
is natively supported by the OpenAI Agents SDK via `MCPServerStdio`.
The MCP server defines tools as Python functions decorated with
`@server.tool()`, which are auto-discovered by the agent.

**Key findings**:

- **Package**: `mcp[cli]` (pip install)
- **Server definition**: Create a `Server` instance, define tools
  with `@server.tool()` decorator
- **Tool schema**: Each tool gets name, description, and input
  schema (JSON Schema) automatically from function signature
- **Transport**: Stdio (default) — the SDK runs the MCP server as
  a subprocess and communicates via stdin/stdout
- **Stateless**: Each tool invocation receives all needed context
  (user_id) as a parameter; no state retained between calls
- **Database access**: MCP tool functions import the ORM session
  and call existing `TaskService` methods

**Architecture**:

```
FastAPI endpoint
  └── OpenAI Agent (via Runner.run)
        └── MCPServerStdio(command="python", args=["-m", "backend.src.mcp_server"])
              └── MCP tools: add_task, list_tasks, complete_task, update_task, delete_task
                    └── TaskService (existing) → SQLModel → PostgreSQL
```

**Alternatives considered**:

| Alternative | Why Rejected |
|---|---|
| SSE transport | More complex; no advantage for single-server setup |
| In-process function tools | Not MCP-compliant; constitution requires MCP protocol |
| Separate MCP microservice | Over-engineering; same-process stdio is sufficient |

## R3: Conversation Persistence Strategy

**Decision**: Store conversations and messages in PostgreSQL using
SQLModel, reconstruct full history on each request.

**Rationale**: The stateless architecture mandate requires that no
conversation state lives in server memory. PostgreSQL is the single
source of truth per constitution. Reconstructing history per-request
ensures conversation continuity survives restarts.

**Key findings**:

- **Models**: `Conversation` (id, user_id, timestamps) and `Message`
  (id, conversation_id, user_id, role, content, timestamp)
- **Flow per request**:
  1. Look up or create Conversation for user
  2. Load all Messages for that conversation, ordered by created_at
  3. Convert to agent-compatible message format
  4. Append new user message and persist
  5. Run agent with full history
  6. Persist agent response as new Message
  7. Return response to frontend

**Alternatives considered**:

| Alternative | Why Rejected |
|---|---|
| Redis for conversation cache | Adds infrastructure; constitution says PostgreSQL only |
| In-memory conversation dict | Violates stateless architecture invariant |
| File-based conversation store | Not suitable for production; PostgreSQL mandated |

## R4: Chat API Design

**Decision**: Single endpoint `POST /api/{user_id}/chat` with optional
`conversation_id` and required `message` fields.

**Rationale**: Matches the spec and constitution exactly. A single
endpoint simplifies the frontend integration — ChatKit sends messages
here and renders responses. The optional conversation_id allows the
system to auto-create conversations for new users.

**Key findings**:

- **Request schema**: `{ conversation_id?: string, message: string }`
- **Response schema**: `{ conversation_id: string, response: string, tool_calls?: list }`
- **Auto-creation**: If no conversation_id, create new Conversation
- **Ownership**: user_id from URL path; all operations scoped to user
- **Error format**: `{ detail: string }` with HTTP status codes

## R5: Frontend Integration (ChatKit)

**Decision**: Use OpenAI ChatKit React component connected to the
backend chat API endpoint.

**Rationale**: ChatKit is a pre-built chat UI component from OpenAI
that handles message rendering, input, and conversation display.
It minimizes frontend development effort and keeps the frontend as
a thin client per constitution.

**Key findings**:

- **Package**: `@openai/chat-kit` (npm install)
- **Integration**: Configure with API endpoint URL and auth headers
- **Message format**: ChatKit expects `{ role, content }` pairs
- **Customization**: Supports custom message renderers and themes
- **State**: ChatKit manages local UI state; server is source of truth

## R6: MCP Tool-to-Service Mapping

**Decision**: Each MCP tool maps directly to an existing `TaskService`
method, wrapped with user_id validation and structured output.

**Mapping**:

| MCP Tool | TaskService Method | Input | Output |
|---|---|---|---|
| `add_task` | `create_task` | user_id, title, description? | Task dict |
| `list_tasks` | `get_tasks_by_user` | user_id | List of task dicts |
| `complete_task` | `toggle_task_completion` | user_id, task_id | Task dict |
| `update_task` | `update_task` | user_id, task_id, title?, description? | Task dict |
| `delete_task` | `delete_task` | user_id, task_id | Success bool |

**Rationale**: Reuses existing Phase II service layer; MCP tools are
thin wrappers that add structured I/O and user ownership validation.

## R7: Authentication Integration

**Decision**: Better Auth provides user identity; user_id in URL path
is validated against the authenticated session.

**Rationale**: Phase II already has Better Auth with JWT. The chat
endpoint uses the same auth middleware to extract user_id and ensure
the path parameter matches the authenticated user.

**Key findings**:

- Existing `auth_handler.py` and `middleware.py` provide JWT validation
- `user_id` path parameter MUST match JWT-extracted user identity
- MCP tools receive user_id as a parameter from the chat endpoint
- No additional auth infrastructure needed
