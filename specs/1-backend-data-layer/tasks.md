---
description: "Task list for Core Backend & Data Layer implementation"
---

# Tasks: Core Backend & Data Layer for Todo Full-Stack Web Application

**Input**: Design documents from `/specs/1-backend-data-layer/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 Initialize Python project with FastAPI and SQLModel dependencies in requirements.txt
- [X] T003 [P] Configure linting and formatting tools (black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework in backend/src/database/database.py
- [X] T005 [P] Implement authentication/authorization framework in backend/src/auth/
- [X] T006 [P] Setup API routing and middleware structure in backend/src/main.py
- [X] T007 Create base models/entities that all stories depend on in backend/src/models/__init__.py
- [X] T008 Configure error handling and logging infrastructure in backend/src/utils/
- [X] T009 Setup environment configuration management in backend/.env.example and backend/src/config.py
- [X] T010 [P] Configure automated testing framework aligned with constitutional requirements in backend/pytest.ini
- [X] T011 [P] Set up spec-first development workflow with requirement tracing in backend/docs/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks in their personal task list with proper user association

**Independent Test**: Can be fully tested by sending a POST request to create a task and verifying it's stored in the database with the correct user association, delivering the ability to persist user data.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T012 [P] [US1] Contract test for POST /api/{user_id}/tasks in backend/tests/contract/test_task_creation.py
- [X] T013 [P] [US1] Integration test for task creation user journey in backend/tests/integration/test_task_creation.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Create Task model in backend/src/models/task_model.py
- [X] T015 [P] [US1] Create TaskCreate and TaskResponse Pydantic schemas in backend/src/schemas/task_schemas.py
- [X] T016 [US1] Implement TaskService in backend/src/services/task_service.py (depends on T014)
- [X] T017 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/task_routes.py
- [X] T018 [US1] Add validation and error handling for task creation in backend/src/api/task_routes.py
- [X] T019 [US1] Add logging for task creation operations in backend/src/services/task_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Retrieve User Tasks (Priority: P1)

**Goal**: Allow users to view all their tasks with proper user association

**Independent Test**: Can be fully tested by creating tasks for a user and then retrieving them via GET request, delivering the ability to access user data.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T020 [P] [US2] Contract test for GET /api/{user_id}/tasks in backend/tests/contract/test_task_retrieval.py
- [X] T021 [P] [US2] Integration test for task retrieval user journey in backend/tests/integration/test_task_retrieval.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Add TaskResponseList schema in backend/src/schemas/task_schemas.py
- [X] T023 [US2] Extend TaskService with get_user_tasks method in backend/src/services/task_service.py
- [X] T024 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/task_routes.py
- [X] T025 [US2] Add validation and error handling for task retrieval in backend/src/api/task_routes.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Specific Task (Priority: P2)

**Goal**: Allow users to view details of a specific task they own

**Independent Test**: Can be fully tested by retrieving a specific task by its ID for a user, delivering the ability to access individual task details.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T026 [P] [US3] Contract test for GET /api/{user_id}/tasks/{id} in backend/tests/contract/test_specific_task.py
- [X] T027 [P] [US3] Integration test for specific task retrieval in backend/tests/integration/test_specific_task.py

### Implementation for User Story 3

- [X] T028 [US3] Extend TaskService with get_task_by_id method in backend/src/services/task_service.py
- [X] T029 [US3] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/task_routes.py
- [X] T030 [US3] Add proper user ownership validation for specific task access in backend/src/services/task_service.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P2)

**Goal**: Enable users to modify details of tasks they own

**Independent Test**: Can be fully tested by updating a specific task and verifying the changes are persisted, delivering the ability to modify user data.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T031 [P] [US4] Contract test for PUT /api/{user_id}/tasks/{id} in backend/tests/contract/test_task_update.py
- [X] T032 [P] [US4] Integration test for task update journey in backend/tests/integration/test_task_update.py

### Implementation for User Story 4

- [X] T033 [P] [US4] Create TaskUpdate Pydantic schema in backend/src/schemas/task_schemas.py
- [X] T034 [US4] Extend TaskService with update_task method in backend/src/services/task_service.py
- [X] T035 [US4] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/task_routes.py
- [X] T036 [US4] Add proper user ownership validation for task updates in backend/src/services/task_service.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Allow users to remove tasks they own

**Independent Test**: Can be fully tested by deleting a specific task and verifying it's removed from storage, delivering the ability to remove user data.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T037 [P] [US5] Contract test for DELETE /api/{user_id}/tasks/{id} in backend/tests/contract/test_task_deletion.py
- [X] T038 [P] [US5] Integration test for task deletion journey in backend/tests/integration/test_task_deletion.py

### Implementation for User Story 5

- [X] T039 [US5] Extend TaskService with delete_task method in backend/src/services/task_service.py
- [X] T040 [US5] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/task_routes.py
- [X] T041 [US5] Add proper user ownership validation for task deletion in backend/src/services/task_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Documentation updates in backend/docs/
- [X] T043 Code cleanup and refactoring
- [X] T044 Performance optimization across all stories
- [X] T045 [P] Additional unit tests (if requested) in backend/tests/unit/
- [X] T046 Security hardening for user isolation
- [X] T047 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/{user_id}/tasks in backend/tests/contract/test_task_creation.py"
Task: "Integration test for task creation user journey in backend/tests/integration/test_task_creation.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task_model.py"
Task: "Create TaskCreate and TaskResponse Pydantic schemas in backend/src/schemas/task_schemas.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Constitutional Compliance Validation

### Spec-First Development Tasks
- [X] T048 Verify all implemented features trace back to approved spec requirements
- [X] T049 Confirm implementation matches spec-defined REST contract behavior
- [X] T050 Validate that no code was manually written outside agent-generated outputs

### Security Validation Tasks
- [X] T051 Test that backend rejects unauthenticated requests with 401 Unauthorized
- [X] T052 Verify that cross-user data access is impossible
- [X] T053 Confirm JWT token verification uses shared secret across services
- [X] T054 Validate that database schema supports multi-user isolation
- [X] T055 Test that frontend attaches JWT to every API request
- [X] T056 Verify no secrets are hardcoded in the codebase

### Tech Stack Compliance Tasks
- [X] T057 Confirm all components use approved technology stack (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT)
- [X] T058 Verify REST API endpoints remain stable and consistent
- [X] T059 Validate all authenticated requests require valid JWT
- [X] T060 Confirm stateless backend authentication (no shared sessions)

### Success Criteria Validation Tasks
- [X] T061 Test end-to-end flow: signup → login → CRUD tasks → logout
- [X] T062 Verify each user can only see and modify their own tasks
- [X] T063 Run negative test cases to verify API security
- [X] T064 Confirm all specs pass implementation review without deviation

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitutional compliance tasks must be completed to ensure adherence to project principles