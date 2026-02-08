---
id: 1
title: "Phase III Master Specification"
stage: spec
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 004-todo-ai-chatbot
branch: 004-todo-ai-chatbot
user: user
command: "/sp.specify"
labels: ["spec", "phase-iii", "ai-chatbot", "mcp", "master-spec"]
links:
  spec: specs/004-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-todo-ai-chatbot/spec.md
  - specs/004-todo-ai-chatbot/checklists/requirements.md
  - history/prompts/004-todo-ai-chatbot/1-phase-iii-master-specification.spec.prompt.md
tests:
  - Spec quality checklist: all 16 items PASS
  - No NEEDS CLARIFICATION markers remaining
  - All 7 user stories have acceptance scenarios
  - All 17 functional requirements use MUST language
---

## Prompt

spec-4

Phase III: Todo AI Chatbot (Master Specification)

1. Purpose

Build an AI-powered Todo chatbot that manages tasks via natural language using OpenAI Agents SDK and MCP (Model Context Protocol), with the agent backend fully integrated with the frontend chat UI, while maintaining a stateless backend and persistent conversations in PostgreSQL.

2. Scope

This phase introduces:

Conversational task management

Agent-driven reasoning

MCP-based tool invocation

Stateless chat API with durable memory

End-to-end integration between ChatKit frontend and agent-powered backend

Out of scope:

Advanced analytics

Notifications

Manual task editing outside chat

Multi-agent orchestration

3. System Principles (Hard Constraints)

Backend servers are stateless

PostgreSQL is the single source of truth

AI agents never access the database directly

All task mutations occur via MCP tools

Conversation state is reconstructed per request

Frontend never calls MCP or database directly

Frontend communicates only with the agent backend via chat API

4. Technology Stack

Frontend: OpenAI ChatKit

Backend: FastAPI (Python)

AI Framework: OpenAI Agents SDK

MCP Server: Official MCP SDK

ORM: SQLModel

Database: Neon Serverless PostgreSQL

Auth: Better Auth

5. High-Level Architecture

Flow:

User interacts with ChatKit UI

ChatKit sends message to FastAPI /api/{user_id}/chat

Backend loads conversation history from DB

Agent runs with context and MCP tools

MCP server performs task operations

Results persisted to DB

Backend returns agent response to frontend

ChatKit renders assistant reply

The frontend remains a thin client with no business logic.

6. Core Features

Add, list, update, complete, and delete tasks via chat

Natural language understanding via agent backend

Action confirmations returned to frontend

Graceful error messaging surfaced in UI

Conversations resume seamlessly after restart

7. Data Models (Canonical)

Task: id, user_id, title, description, completed, created_at, updated_at

Conversation: id, user_id, created_at, updated_at

Message: id, conversation_id, user_id, role, content, created_at

No model drift allowed.

8. Chat API Contract

POST /api/{user_id}/chat

Request:

conversation_id (optional)

message (required)

Response:

conversation_id

response

tool_calls

This endpoint is the only integration point between frontend and agent backend.

9. MCP Tool Authority

The agent may only use:

add_task

list_tasks

update_task

complete_task

delete_task

MCP tools:

Are stateless

Validate user ownership

Persist changes via ORM

Return structured outputs

10. Integration Guarantees

Frontend receives only finalized assistant messages

Tool execution details are optional and non-blocking for UI

Backend shields frontend from MCP and agent internals

API remains stable regardless of agent or MCP changes

11. Success Criteria

Phase III is complete when:

Frontend and agent backend communicate end-to-end

Tasks are managed via natural language in the UI

MCP tools are the only mutation boundary

Stateless server with persistent conversations

## Response snapshot

Created the Phase III master specification at `specs/004-todo-ai-chatbot/spec.md` with:

- **7 user stories** covering the complete task management lifecycle:
  - P1: Add Task, List Tasks
  - P2: Complete Task, Update Task, Delete Task
  - P3: Conversation Persistence, Multi-Step Agent Reasoning
- **17 functional requirements** (FR-001 through FR-017) all using MUST/MUST NOT language
- **3 canonical entities**: Task, Conversation, Message
- **7 measurable success criteria** + 9 constitutional compliance outcomes
- **6 edge cases** with expected behaviors
- **5 assumptions** documented
- **0 NEEDS CLARIFICATION markers** — user input was comprehensive
- Quality checklist created at `specs/004-todo-ai-chatbot/checklists/requirements.md` — all 16 items PASS

## Outcome

- ✅ Impact: Complete master specification for Phase III AI chatbot feature
- 🧪 Tests: Quality checklist 16/16 PASS, 0 clarification markers
- 📁 Files: spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.clarify (optional) or /sp.plan to begin implementation planning
- 🧠 Reflection: User provided exceptionally detailed input covering all 11 sections; no clarification needed

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script had parameter binding error on multi-line input; directory still created successfully
- Graders run and results (PASS/FAIL): Quality checklist ALL PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.plan for implementation planning
