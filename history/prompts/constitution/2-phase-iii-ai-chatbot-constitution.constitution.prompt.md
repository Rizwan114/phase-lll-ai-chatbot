---
id: 2
title: "Phase III AI Chatbot Constitution"
stage: constitution
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: none
branch: main
user: user
command: "/sp.constitution"
labels: ["constitution", "phase-iii", "ai-chatbot", "mcp", "stateless"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
  - history/prompts/constitution/2-phase-iii-ai-chatbot-constitution.constitution.prompt.md
tests:
  - Constitution validation: no unresolved placeholders
  - Template sync: all three templates updated with Phase III checks
  - Version coherence: 1.1.0 → 2.0.0 MAJOR bump verified
---

## Prompt

Phase III: Todo AI Chatbot
Role & Authority

You are an expert autonomous software engineer and system architect operating inside an Agentic Development Stack.
You must strictly follow the specifications provided and never invent requirements, tools, APIs, or behavior beyond what is explicitly defined.

You are building Phase III: Todo AI Chatbot, an AI-powered, stateless, MCP-driven task management system.

You are allowed to:

Generate plans

Break plans into tasks

Implement code only through Claude Code

Iterate when errors occur

You are NOT allowed to:

Manually code outside the agent workflow

Bypass MCP tools

Store server-side state outside the database

Assume undocumented features

Core Development Rules

Spec-First Discipline

Do nothing until the relevant spec is fully understood

If ambiguity exists, ask for clarification instead of guessing

Agentic Workflow Enforcement

Follow this order strictly:

Read Spec → Generate Plan → Break into Tasks → Implement → Validate


Never skip steps

No Manual Coding

All implementation must be generated via Claude Code

Treat Claude Code as the sole executor of code changes

System Architecture Invariants

These rules are non-negotiable:

The FastAPI server is stateless

All state is persisted in PostgreSQL (Neon)

AI agents never access the database directly

AI agents only interact with tasks through MCP tools

MCP tools are stateless and persist data via ORM

Conversation state is reconstructed from the database on every request

If a solution violates any invariant, it is invalid.

AI Agent Behavior Constraints

The AI agent must:

Use OpenAI Agents SDK

Select MCP tools based on user intent

Perform multi-step reasoning when required (e.g., list → delete)

Always confirm successful actions in natural language

Gracefully handle errors (missing task, invalid ID, empty list)

Never hallucinate task IDs or user data

Never fabricate tool outputs

The agent must only use these MCP tools:

add_task

list_tasks

complete_task

update_task

delete_task

MCP Tool Contract Rules

MCP tools define the only mutation boundary

Tools must:

Validate input

Enforce user ownership

Return structured, predictable output

Errors must be explicit and machine-readable

Tool behavior must exactly match the MCP specification

Chat API Rules

Endpoint: POST /api/{user_id}/chat

Each request:

Fetches conversation history

Appends user message

Runs the agent

Persists assistant response

The server must not retain memory between requests

Conversation continuity must survive restarts

Data Model Authority

The following models are canonical and must not drift:

Task

Conversation

Message

No additional fields or models may be introduced unless explicitly approved.

Output Quality Standards

All generated artifacts must be:

Deterministic

Reviewable

Modular

Minimal but complete

Aligned with the provided specs

If tradeoffs exist, prioritize correctness and protocol integrity over convenience.

Error & Recovery Policy

When something fails:

Identify the failure source

## Response snapshot

Updated the project constitution from v1.1.0 to v2.0.0 (MAJOR bump) to reflect Phase III: Todo AI Chatbot architecture. Key changes:

**Principles redefined (6 renamed/redefined, 2 added):**
- I. Spec-First Discipline (strengthened from "Spec-First Development")
- II. Stateless Architecture Invariants (redefined from "Correctness and Consistency")
- III. Data Integrity and User Isolation (narrowed from "Security-by-Design")
- IV. Agentic Workflow Enforcement (expanded from "Automation Over Manual Work")
- V. Tech Stack Compliance (updated stack: removed Better Auth/JWT, added OpenAI Agents SDK/MCP)
- VI. MCP Tool Contract Integrity (new focus, replaces "Quality and Validation Standards")
- VII. AI Agent Behavior Constraints (new)
- VIII. Error and Recovery Policy (new)

**New sections:** Chat API Contract, Canonical Data Models (Task, Conversation, Message).

**Removed:** Better Auth + JWT, frontend-specific rules, REST CRUD endpoints.

**Templates updated:** plan-template.md, spec-template.md, tasks-template.md — all constitutional compliance checks rewritten for Phase III.

## Outcome

- ✅ Impact: MAJOR constitution rewrite for Phase III AI chatbot architecture
- 🧪 Tests: No unresolved placeholders; template sync verified; version coherence confirmed
- 📁 Files: constitution.md, plan-template.md, spec-template.md, tasks-template.md
- 🔁 Next prompts: /sp.specify for Phase III feature spec, /sp.plan for implementation plan
- 🧠 Reflection: Clean separation between Phase II (REST CRUD) and Phase III (MCP-driven chatbot) principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Template sync PASS, placeholder check PASS, version coherence PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.specify to create Phase III feature spec
