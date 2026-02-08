# Tasks: Phase 1 CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-interface.md, research.md, quickstart.md

**Tests**: Included - The plan specifies 90%+ test coverage with unit and integration tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

All work is contained in the `/phase-1` directory as per Phase 1 scope requirements.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure in /phase-1 directory

- [x] T001 Create phase-1 directory structure with src/, tests/, and subdirectories per plan.md
- [x] T002 Initialize UV project in phase-1/ with pyproject.toml for Python 3.13+
- [x] T003 Create .python-version file in phase-1/ specifying Python 3.13
- [x] T004 [P] Add development dependencies to pyproject.toml: pytest, pytest-cov, ruff
- [x] T005 [P] Create all __init__.py files in phase-1/src/ and phase-1/tests/ directories
- [x] T006 [P] Configure ruff settings in pyproject.toml for linting and formatting

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain model and infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create TaskStatus enum in phase-1/src/models/task.py with PENDING and COMPLETE values
- [x] T008 Create Task dataclass in phase-1/src/models/task.py with id, description, status fields
- [x] T009 Add validation logic to Task model for non-empty description and 500 char limit
- [x] T010 Create custom exception classes in phase-1/src/utils/validators.py: ValidationError, TaskNotFoundError
- [x] T011 Create TaskService class in phase-1/src/services/task_service.py with in-memory dict storage
- [x] T012 Implement ID generation logic in TaskService using auto-incrementing counter

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks and view all tasks with their status

**Independent Test**: Add multiple tasks and list them. Verify tasks display with ID, description, and status. Verify empty state message when no tasks exist.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [P] [US1] Unit test for Task model validation in phase-1/tests/unit/test_task.py
- [x] T014 [P] [US1] Unit test for TaskService.add_task in phase-1/tests/unit/test_task_service.py
- [x] T015 [P] [US1] Unit test for TaskService.get_all_tasks in phase-1/tests/unit/test_task_service.py
- [x] T016 [P] [US1] Unit test for display formatting in phase-1/tests/unit/test_display.py

### Implementation for User Story 1

- [x] T017 [US1] Implement TaskService.add_task method in phase-1/src/services/task_service.py
- [x] T018 [US1] Implement TaskService.get_all_tasks method in phase-1/src/services/task_service.py
- [x] T019 [P] [US1] Create display.py in phase-1/src/cli/ with format_task_list function
- [x] T020 [P] [US1] Create display.py format_success_message and format_error_message functions
- [x] T021 [US1] Create TodoCLI class extending cmd.Cmd in phase-1/src/cli/commands.py
- [x] T022 [US1] Implement do_add command handler in phase-1/src/cli/commands.py
- [x] T023 [US1] Implement do_list command handler in phase-1/src/cli/commands.py
- [x] T024 [US1] Add help text for add and list commands in phase-1/src/cli/commands.py
- [x] T025 [US1] Integration test for add and list commands in phase-1/tests/integration/test_cli_commands.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add and list tasks.

---

## Phase 4: User Story 2 - Mark Tasks as Complete (Priority: P2)

**Goal**: Users can mark tasks as complete to track progress

**Independent Test**: Add tasks, mark some as complete, verify status changes are reflected in list view. Verify idempotent behavior (marking already-complete task).

### Tests for User Story 2

- [x] T026 [P] [US2] Unit test for TaskService.mark_complete in phase-1/tests/unit/test_task_service.py
- [x] T027 [P] [US2] Unit test for idempotent complete operation in phase-1/tests/unit/test_task_service.py

### Implementation for User Story 2

- [x] T028 [US2] Implement TaskService.mark_complete method in phase-1/src/services/task_service.py
- [x] T029 [US2] Implement do_complete command handler in phase-1/src/cli/commands.py
- [x] T030 [US2] Add help text for complete command in phase-1/src/cli/commands.py
- [x] T031 [US2] Integration test for complete command in phase-1/tests/integration/test_cli_commands.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, list, and complete tasks.

---

## Phase 5: User Story 3 - Update Task Description (Priority: P3)

**Goal**: Users can update task descriptions to correct mistakes or refine details

**Independent Test**: Create task, update its description, verify change persists in list view. Verify validation (empty description rejected).

### Tests for User Story 3

- [x] T032 [P] [US3] Unit test for TaskService.update_task in phase-1/tests/unit/test_task_service.py
- [x] T033 [P] [US3] Unit test for update validation (empty description) in phase-1/tests/unit/test_task_service.py

### Implementation for User Story 3

- [x] T034 [US3] Implement TaskService.update_task method in phase-1/src/services/task_service.py
- [x] T035 [US3] Implement do_update command handler in phase-1/src/cli/commands.py
- [x] T036 [US3] Add help text for update command in phase-1/src/cli/commands.py
- [x] T037 [US3] Integration test for update command in phase-1/tests/integration/test_cli_commands.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Users can add, list, complete, and update tasks.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks to keep their list clean and focused

**Independent Test**: Create tasks, delete specific ones, verify they no longer appear in list. Verify error handling for non-existent task IDs.

### Tests for User Story 4

- [x] T038 [P] [US4] Unit test for TaskService.delete_task in phase-1/tests/unit/test_task_service.py
- [x] T039 [P] [US4] Unit test for delete with non-existent ID in phase-1/tests/unit/test_task_service.py

### Implementation for User Story 4

- [x] T040 [US4] Implement TaskService.delete_task method in phase-1/src/services/task_service.py
- [x] T041 [US4] Implement do_delete command handler in phase-1/src/cli/commands.py
- [x] T042 [US4] Add help text for delete command in phase-1/src/cli/commands.py
- [x] T043 [US4] Integration test for delete command in phase-1/tests/integration/test_cli_commands.py

**Checkpoint**: All user stories should now be independently functional. Full CRUD operations available.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final verification

- [x] T044 [P] Implement do_help command handler in phase-1/src/cli/commands.py
- [x] T045 [P] Implement do_exit command handler in phase-1/src/cli/commands.py
- [x] T046 Create main.py entry point in phase-1/src/ with welcome message and REPL startup
- [x] T047 Add error handling for all edge cases in phase-1/src/cli/commands.py
- [x] T048 [P] Create input validators in phase-1/src/utils/validators.py for task ID and description
- [x] T049 [P] Unit tests for validators in phase-1/tests/unit/test_validators.py
- [x] T050 Run full test suite and verify 90%+ coverage: pytest phase-1/tests/ --cov=phase-1/src
- [x] T051 Run ruff linter and fix any issues: ruff check phase-1/src/ phase-1/tests/
- [x] T052 Format code with ruff: ruff format phase-1/src/ phase-1/tests/
- [x] T053 Create README.md in phase-1/ with setup instructions, usage examples, and quickstart guide
- [x] T054 Manual verification of all acceptance scenarios from spec.md
- [x] T055 Performance test with 100 tasks to verify <1 second response time

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but builds on same foundation
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent of US1/US2/US3

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Service methods before CLI command handlers
- Command handlers before integration tests
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks can run sequentially (they build on each other)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Within Polish phase, tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Task model validation in phase-1/tests/unit/test_task.py"
Task: "Unit test for TaskService.add_task in phase-1/tests/unit/test_task_service.py"
Task: "Unit test for TaskService.get_all_tasks in phase-1/tests/unit/test_task_service.py"
Task: "Unit test for display formatting in phase-1/tests/unit/test_display.py"

# After tests fail, launch parallel implementation tasks:
Task: "Create display.py in phase-1/src/cli/ with format_task_list function"
Task: "Create display.py format_success_message and format_error_message functions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T025)
4. Complete Phase 7: Minimal polish (T046, T053) - Just main.py and README
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Demo MVP: Users can add and list tasks

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP!)
3. Add User Story 2 → Test independently → Demo (can now complete tasks)
4. Add User Story 3 → Test independently → Demo (can now update tasks)
5. Add User Story 4 → Test independently → Demo (can now delete tasks)
6. Complete Polish → Final verification and documentation
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T013-T025)
   - Developer B: User Story 2 (T026-T031)
   - Developer C: User Story 3 (T032-T037)
   - Developer D: User Story 4 (T038-T043)
3. Stories complete and integrate independently
4. Team completes Polish together

---

## Task Summary

**Total Tasks**: 55
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 6 tasks
- Phase 3 (User Story 1 - MVP): 13 tasks
- Phase 4 (User Story 2): 6 tasks
- Phase 5 (User Story 3): 6 tasks
- Phase 6 (User Story 4): 6 tasks
- Phase 7 (Polish): 12 tasks

**Parallel Opportunities**: 20 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1: Add 3 tasks, list them, verify display
- US2: Add task, mark complete, verify status change
- US3: Add task, update description, verify change
- US4: Add task, delete it, verify removal

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) + Minimal Phase 7 = 27 tasks

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All work contained in /phase-1 directory per Phase 1 scope
- No file or database persistence - in-memory only
- Python 3.13+ and UV required
- 90%+ test coverage target
