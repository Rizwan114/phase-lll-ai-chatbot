---
id: 1
title: "Update Todo App Constitution"
stage: constitution
date_iso: 2026-02-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: "/sp.constitution"
labels: ["constitution", "todo-app", "spec-driven-development"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

# Prompt History Record

## Metadata
- **ID**: 1
- **Title**: Update Todo App Constitution
- **Stage**: constitution
- **Date**: 2026-02-02-01
- **Surface**: agent
- **Model**: claude-sonnet-4-5-20250929
- **Feature**: none
- **Branch**: main
- **User**: user
- **Command**: /sp.constitution

## Labels
["constitution", "todo-app", "spec-driven-development"]

## Links
- **SPEC**: null
- **TICKET**: null
- **ADR**: null
- **PR**: null

## Files Modified
- .specify/memory/constitution.md
- .specify/templates/plan-template.md
- .specify/templates/spec-template.md
- .specify/templates/tasks-template.md
- history/prompts/constitution/1-update-todo-app-constitution.constitution.prompt.md

## Tests Performed
- Constitution file updated with specific principles
- Template files updated to align with new constitution
- Constitutional compliance checks added to templates

## Prompt Text

```
/sp.constitution

Project: Todo Full-Stack Web Application (Spec-Driven, Agentic Dev Stack)

Core principles:
- Spec-first development (all implementation must trace back to approved specs)
- Correctness and consistency across frontend, backend, and database
- Security-by-design (authentication, authorization, and data isolation enforced)
- Automation over manual work (no handwritten code outside agent-generated outputs)
- Clarity for reviewers (hackathon judges and technical evaluators)

Key standards:
- Every feature must map directly to a written spec requirement
- API behavior must exactly match the defined REST contract
- Authentication must use Better Auth with JWT-based verification
- All backend routes must enforce user ownership and access control
- Frontend, backend, and database must integrate without implicit assumptions
- All secrets handled via environment variables (no hardcoding)

Constraints:
- No manual coding; all code generated via Claude Code using Spec-Kit Plus
- Must use the defined tech stack only:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth + JWT
- REST API endpoints must remain stable and consistent
- All authenticated requests must require a valid JWT
- Stateless backend authentication (no shared sessions)

Quality & validation requirements:
- Backend must reject unauthenticated requests with 401 Unauthorized
- Cross-user data access must be impossible
- JWT token verification must use a shared secret across services
- Database schema must support multi-user isolation
- Frontend must attach JWT to every API request
- Errors must be explicit, consistent, and debuggable

Success criteria:
- All specs pass implementation review without deviation
- End-to-end flow works: signup → login → CRUD tasks → logout
- Each user can only see and modify their own tasks
- API security verified via negative test cases
- Project can be evaluated solely by reviewing specs, plans, prompts
```

## Response Text

Updated the project constitution with specific principles for the Todo Full-Stack Web Application, including spec-first development, correctness and consistency, security-by-design, automation over manual work, tech stack compliance, and quality standards. Updated template files to align with constitutional requirements and added constitutional compliance checks to the plan, spec, and tasks templates.

## Outcome

Successfully created and updated the constitution file with 6 core principles and updated all related templates to ensure constitutional compliance throughout the development process.

## Evaluation

The constitution has been successfully updated and templates have been modified to enforce constitutional compliance. The version has been incremented from 1.0.0 to 1.1.0 to reflect the addition of specific principles for the Todo application.