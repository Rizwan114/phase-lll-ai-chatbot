---
id: 3
title: "Phase III Task Generation"
stage: tasks
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 004-todo-ai-chatbot
branch: 004-todo-ai-chatbot
user: user
command: "/sp.tasks"
labels: ["tasks", "phase-iii", "ai-chatbot", "mcp", "implementation"]
links:
  spec: specs/004-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-todo-ai-chatbot/tasks.md
  - history/prompts/004-todo-ai-chatbot/3-phase-iii-task-generation.tasks.prompt.md
tests:
  - All 82 tasks follow checklist format (checkbox + ID + labels + file paths)
  - Tasks organized by user story phases matching spec priorities
  - Constitutional compliance validation section included
---

## Prompt

spec-4

Spec Check
Review spec-4 and sp.constitution; confirm statelessness and frontend ↔ backend flow.

Models
Implement SQLModel schemas: Task, Conversation, Message.

Migrations
Create and apply Neon PostgreSQL migrations.

MCP Server
Implement MCP server with task tools (add, list, update, complete, delete).

Agent Setup
Configure OpenAI Agent and register MCP tools.

Chat API
Implement POST /api/{user_id}/chat with conversation replay and persistence.

Frontend Hookup
Connect ChatKit UI to chat API and render responses.

Auth
Integrate Better Auth and enforce user identity.

Error Handling
Handle task-not-found, empty lists, and invalid input.

E2E Test
Validate all natural language task flows and restart safety.

## Response snapshot

Generated `specs/004-todo-ai-chatbot/tasks.md` with 82 tasks across 11 phases:

- **Phase 1: Setup** (4 tasks) — Dependencies, config, directory structure
- **Phase 2: Foundational** (16 tasks) — Models, services, MCP server (5 tools), agent, chat API, auth
- **Phase 3: US1+US2** (5 tasks) — Add + List tasks via chat (P1 MVP)
- **Phase 4: US3** (3 tasks) — Complete task via chat (P2)
- **Phase 5: US4** (3 tasks) — Update task via chat (P2)
- **Phase 6: US5** (3 tasks) — Delete task via chat (P2)
- **Phase 7: US6** (4 tasks) — Conversation persistence (P3)
- **Phase 8: US7** (2 tasks) — Multi-step reasoning (P3)
- **Phase 9: Frontend** (7 tasks) — ChatKit UI integration
- **Phase 10: Error Handling** (5 tasks) — Edge cases
- **Phase 11: Polish** (5 tasks) — Final validation
- **Constitutional Compliance** (25 tasks) — Validation checklist

**Key stats**: 82 total tasks, 57 implementation + 25 compliance validation. MVP at Phase 3 (25 tasks). Full completion at Phase 11 (57 tasks + 25 validation).

## Outcome

- ✅ Impact: Complete task breakdown for Phase III with dependency-ordered execution
- 🧪 Tests: All tasks follow checklist format; user story organization matches spec
- 📁 Files: tasks.md
- 🔁 Next prompts: /sp.implement to begin executing tasks
- 🧠 Reflection: User's 10-step outline mapped cleanly to the 7 implementation layers from plan.md

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Format validation PASS, story coverage PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.implement to start Phase 1 setup tasks
