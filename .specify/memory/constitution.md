<!--
Sync Impact Report:
- Version change: 1.1.0 → 2.0.0
- Modified principles:
  - "Spec-First Development" → "Spec-First Discipline" (renamed, strengthened)
  - "Correctness and Consistency" → "Stateless Architecture Invariants" (redefined)
  - "Security-by-Design" → "Data Integrity and User Isolation" (narrowed scope)
  - "Automation Over Manual Work" → "Agentic Workflow Enforcement" (expanded)
  - "Tech Stack Compliance" → "Tech Stack Compliance" (updated stack)
  - "Quality and Validation Standards" → "MCP Tool Contract Integrity" (new focus)
- Added sections:
  - Principle VII: AI Agent Behavior Constraints
  - Principle VIII: Error and Recovery Policy
  - Canonical Data Models section
  - Chat API Contract section
- Removed sections:
  - Better Auth + JWT references (not in Phase III scope)
  - Frontend-specific rules (Phase III is backend/AI-focused)
  - REST CRUD endpoint references (replaced by MCP + chat API)
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Phase III: Todo AI Chatbot Constitution

## Core Principles

### I. Spec-First Discipline

All implementation MUST trace back to an approved specification.
No code MUST be written without a corresponding spec requirement.
If ambiguity exists in any requirement, the agent MUST ask for
clarification instead of guessing. Every MCP tool, API endpoint,
data model, and agent behavior MUST be documented in spec before
development begins.

**Rationale**: Prevents drift between intent and implementation;
ensures all artifacts are reviewable and auditable.

### II. Stateless Architecture Invariants

These rules are non-negotiable and MUST NOT be violated:

- The FastAPI server MUST be stateless.
- All state MUST be persisted in PostgreSQL (Neon).
- AI agents MUST NOT access the database directly.
- AI agents MUST only interact with tasks through MCP tools.
- MCP tools MUST be stateless and persist data via ORM.
- Conversation state MUST be reconstructed from the database
  on every request.
- The server MUST NOT retain memory between requests.
- Conversation continuity MUST survive server restarts.

**Rationale**: Stateless design guarantees horizontal scalability,
reproducible behavior, and eliminates hidden coupling between
requests.

### III. Data Integrity and User Isolation

- User ownership MUST be enforced at the MCP tool layer.
- Cross-user data access MUST be impossible by design.
- All secrets MUST be handled via environment variables;
  hardcoding is prohibited.
- Database schema MUST support multi-user isolation.

**Rationale**: Each user's data is a trust boundary; violations
are security defects regardless of severity.

### IV. Agentic Workflow Enforcement

All implementation MUST follow this order strictly:

1. Read Spec
2. Generate Plan
3. Break into Tasks
4. Implement (via Claude Code only)
5. Validate

- No manual coding outside the agent workflow is permitted.
- All code MUST be generated via Claude Code.
- Claude Code is the sole executor of code changes.
- No steps may be skipped.

**Rationale**: Enforces traceability, repeatability, and ensures
every change is auditable through the spec-driven pipeline.

### V. Tech Stack Compliance

The following technology stack is mandatory. Deviations require
explicit approval and updated specifications:

- **Server Framework**: Python FastAPI (stateless)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **AI Agent SDK**: OpenAI Agents SDK
- **Tool Protocol**: MCP (Model Context Protocol)
- **State Management**: Database-only (no in-memory state)

**Rationale**: A locked stack prevents technology sprawl and
ensures all team members and agents operate on shared
assumptions.

### VI. MCP Tool Contract Integrity

MCP tools define the ONLY mutation boundary in the system.
The AI agent MUST only use these MCP tools:

- `add_task`
- `list_tasks`
- `complete_task`
- `update_task`
- `delete_task`

All MCP tools MUST:

- Validate input before processing.
- Enforce user ownership on every operation.
- Return structured, predictable output.
- Produce explicit, machine-readable errors.
- Behave exactly as specified in the MCP specification.

**Rationale**: A single mutation boundary eliminates
inconsistency between data paths and makes the system
auditable at the tool layer.

### VII. AI Agent Behavior Constraints

The AI agent MUST:

- Use the OpenAI Agents SDK.
- Select MCP tools based on user intent.
- Perform multi-step reasoning when required
  (e.g., list then delete).
- Always confirm successful actions in natural language.
- Gracefully handle errors (missing task, invalid ID,
  empty list).
- Never hallucinate task IDs or user data.
- Never fabricate tool outputs.

**Rationale**: The agent is the user-facing interface;
incorrect or fabricated responses erode trust and corrupt
data.

### VIII. Error and Recovery Policy

When something fails, the system MUST:

1. Identify the failure source.
2. Return an explicit, machine-readable error.
3. Never silently swallow exceptions.
4. Never retry destructive operations without confirmation.
5. Log sufficient context for debugging.

**Rationale**: Explicit error handling enables fast diagnosis
and prevents cascading silent failures.

## Chat API Contract

**Endpoint**: `POST /api/{user_id}/chat`

Each request MUST:

1. Fetch conversation history from the database.
2. Append the user message.
3. Run the AI agent with MCP tools.
4. Persist the assistant response to the database.

The server MUST NOT retain memory between requests.
Conversation continuity MUST survive restarts.

## Canonical Data Models

The following models are authoritative and MUST NOT drift:

- **Task**: Represents a user's todo item.
- **Conversation**: Represents a chat session for a user.
- **Message**: Represents a single message in a conversation.

No additional fields or models may be introduced unless
explicitly approved. Schema changes require spec updates.

## Key Standards

- Every feature MUST map directly to a written spec requirement.
- MCP tool behavior MUST exactly match the defined specification.
- All backend routes MUST enforce user ownership and access control.
- All state MUST be persisted in PostgreSQL; no in-memory state.
- All secrets MUST be handled via environment variables.
- AI agent output MUST be deterministic and reproducible given
  the same input and database state.

## Constraints

- No manual coding; all code generated via Claude Code.
- MUST use the defined tech stack only (see Principle V).
- MCP tools are the sole data mutation interface.
- The FastAPI server MUST remain stateless.
- No additional data models without explicit approval.
- No server-side state outside the database.

## Quality and Validation Requirements

- MCP tools MUST validate all inputs.
- Cross-user data access MUST be impossible.
- Database schema MUST support multi-user isolation.
- Errors MUST be explicit, consistent, and debuggable.
- AI agent MUST NOT hallucinate task IDs or fabricate outputs.
- Conversation state MUST survive server restarts.

## Success Criteria

- All specs pass implementation review without deviation.
- End-to-end flow works: user sends chat message, agent
  selects correct MCP tool, tool executes, agent responds
  in natural language.
- Each user can only see and modify their own tasks.
- Multi-step agent reasoning works (e.g., "delete all
  completed tasks" requires list then delete).
- Conversation history persists across server restarts.
- Project can be evaluated solely by reviewing specs,
  plans, and prompts.

## Governance

This constitution governs all Phase III development activities.
All implementations MUST comply with these principles.

### Amendment Procedure

1. Propose change with rationale and impact assessment.
2. Document the change in a new constitution version.
3. Obtain approval from project stakeholders.
4. Update all dependent templates and artifacts.
5. Record the amendment in a PHR.

### Versioning Policy

- **MAJOR**: Backward-incompatible principle removals or
  redefinitions.
- **MINOR**: New principle/section added or materially
  expanded guidance.
- **PATCH**: Clarifications, wording, typo fixes.

### Compliance Review

- All pull requests MUST verify constitutional compliance.
- Code quality, security, and architectural decisions MUST
  align with these principles.
- Constitutional compliance checks are embedded in the
  plan and tasks templates.

**Version**: 2.0.0 | **Ratified**: 2026-02-01 | **Last Amended**: 2026-02-08
