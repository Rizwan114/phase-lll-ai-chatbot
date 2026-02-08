---
id: 2
title: "Phase III Implementation Plan"
stage: plan
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 004-todo-ai-chatbot
branch: 004-todo-ai-chatbot
user: user
command: "/sp.plan"
labels: ["plan", "phase-iii", "ai-chatbot", "mcp", "architecture"]
links:
  spec: specs/004-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-todo-ai-chatbot/plan.md
  - specs/004-todo-ai-chatbot/research.md
  - specs/004-todo-ai-chatbot/data-model.md
  - specs/004-todo-ai-chatbot/quickstart.md
  - specs/004-todo-ai-chatbot/contracts/chat-api.md
  - specs/004-todo-ai-chatbot/contracts/mcp-tools.md
tests:
  - Constitution check: all 7 sections PASS (28/28 items checked)
  - No NEEDS CLARIFICATION markers in technical context
  - All implementation layers documented with dependencies
---

## Prompt

spec-4
Goal

Integrate ChatKit frontend with agent-powered FastAPI backend using MCP tools, keeping the server stateless.

Steps

Spec Validation

Review spec-4 and sp.constitution

Confirm frontend ↔ backend integration rules

Database

Create SQLModel schemas: Task, Conversation, Message

Apply migrations on Neon

MCP Server

Implement MCP server

Expose task tools (add, list, update, complete, delete)

Enforce ownership and validation

Agent Backend

Configure OpenAI Agents SDK

Register MCP tools

Implement intent-based tool selection

Chat API

Implement POST /api/{user_id}/chat

Load conversation history

Persist messages and responses

Return agent output to frontend

Frontend Integration

Connect ChatKit to chat API

Send message + conversation_id

Render agent responses

Auth

Integrate Better Auth

Ensure user_id consistency

Validation

Test all NL commands

Verify statelessness and restart safety

## Response snapshot

Generated the complete implementation plan for Phase III Todo AI Chatbot with 6 design artifacts:

**plan.md**: Full implementation plan with technical context, constitution check (28/28 items passing), project structure (existing + 15 new files), architecture diagram showing request flow from ChatKit through FastAPI/Agent/MCP to PostgreSQL, and 7 implementation layers.

**research.md**: 7 research decisions covering OpenAI Agents SDK (R1), MCP server with stdio transport (R2), conversation persistence strategy (R3), chat API design (R4), ChatKit frontend (R5), MCP-to-service mapping (R6), and Better Auth integration (R7).

**data-model.md**: 3 canonical models — Task (existing, unchanged), Conversation (new, UUID PK, unique user_id), Message (new, FK to conversation, role enum). Includes ERD, migration notes, and query patterns.

**contracts/chat-api.md**: POST /api/{user_id}/chat contract with request/response schemas, error responses (400/401/403/404/422/500), behavior contract (9 steps), and concurrency notes.

**contracts/mcp-tools.md**: 5 MCP tool contracts (add_task, list_tasks, complete_task, update_task, delete_task) with input schemas, success/error output schemas, and service mappings.

**quickstart.md**: Setup guide with prerequisites, backend/frontend setup, test commands, and troubleshooting table.

## Outcome

- ✅ Impact: Complete Phase III architecture designed with 7 implementation layers
- 🧪 Tests: Constitution check 28/28 PASS; no unresolved clarifications
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.md, contracts/mcp-tools.md
- 🔁 Next prompts: /sp.tasks to generate actionable tasks, then /sp.implement
- 🧠 Reflection: Phase II codebase well-structured — Phase III adds modules alongside without modifying existing code

## Evaluation notes (flywheel)

- Failure modes observed: Background research agent timed out; proceeded with training knowledge
- Graders run and results (PASS/FAIL): Constitution check ALL PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.tasks to break plan into implementable tasks
