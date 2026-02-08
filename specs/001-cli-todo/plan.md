# Implementation Plan: Phase 1 CLI Todo Application

**Branch**: `001-cli-todo` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo/spec.md`

## Summary

Build a command-line interface (CLI) todo application in Python 3.13+ that provides five core operations (add, list, update, delete, mark complete) with in-memory task storage. The application will use UV for dependency management, maintain tasks during the session only, and provide clear user feedback with comprehensive error handling. All work is isolated to the `/phase-1` directory to establish the foundational domain logic for future phases.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: UV (package manager), standard Python libraries only (argparse for CLI, dataclasses for models)
**Storage**: In-memory (Python list/dictionary structure)
**Testing**: pytest with coverage reporting
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project (CLI application)
**Performance Goals**: <1 second response time for all operations with up to 100 tasks
**Constraints**:
- All code in `/phase-1` folder
- No file or database persistence
- No external API dependencies
- Session-only data retention
**Scale/Scope**: Support up to 100 tasks without performance degradation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase Isolation ✅
- **Status**: PASS
- **Verification**: All work contained in `/phase-1` directory. No dependencies on other phases. Phase 2 (Todo Full-Stack Web Application) can build on this foundation without modifying Phase 1 code.

### Spec-Driven Development ✅
- **Status**: PASS
- **Verification**: Following strict sequence: Specify (complete) → Plan (in progress) → Tasks (next) → Implement (after tasks)

### Scope Discipline ✅
- **Status**: PASS
- **Verification**: All requirements align with Phase 1 definition in constitution. No web API, no persistence, no authentication - strictly CLI with in-memory storage as defined.

### Protected Directories ✅
- **Status**: PASS
- **Verification**: No modifications to `.specify/`, `.specifyplus/`, or `.speckit/` directories. All work in `/phase-1`.

### Verification-First ✅
- **Status**: PASS
- **Verification**: Each task will include explicit acceptance criteria. Test suite will verify all functional requirements before phase closure.

### Evolutionary Architecture ✅
- **Status**: PASS
- **Verification**: Phase 1 establishes core domain logic (Task entity, CRUD operations) that Phase 2 (Todo Full-Stack Web Application) will extend with persistence and web API without breaking CLI functionality.

**Constitution Compliance**: ALL GATES PASSED - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   └── cli-interface.md # CLI command specifications
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase-1/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task entity and TaskStatus enum
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic for CRUD operations
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands.py      # Command handlers (add, list, update, delete, complete)
│   │   └── display.py       # Output formatting and user feedback
│   └── utils/
│       ├── __init__.py
│       └── validators.py    # Input validation logic
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   ├── test_task_service.py
│   │   ├── test_validators.py
│   │   └── test_display.py
│   └── integration/
│       ├── __init__.py
│       └── test_cli_commands.py
│
├── pyproject.toml           # UV project configuration
├── README.md                # Setup and usage instructions
└── .python-version          # Python version specification (3.13)
```

**Structure Decision**: Single project structure selected because this is a standalone CLI application with no frontend/backend separation. The structure follows Python best practices with clear separation of concerns: models (domain entities), services (business logic), cli (user interface), and utils (cross-cutting concerns). Tests mirror the source structure for easy navigation.

## Complexity Tracking

No constitution violations detected. All requirements align with Phase 1 scope and principles.

## Phase 0: Research & Technical Decisions

### Research Areas

1. **Python CLI Best Practices**
   - Command-line argument parsing strategies
   - User feedback and error message patterns
   - Exit codes and signal handling

2. **Clean Code Principles for Python**
   - Function size and single responsibility
   - Naming conventions (PEP 8)
   - Error handling patterns

3. **In-Memory Data Structure Design**
   - Task storage approach (list vs dict vs both)
   - ID generation strategy
   - Performance characteristics

4. **UV Package Manager**
   - Project initialization
   - Dependency management
   - Development vs production dependencies

5. **Testing Strategy**
   - Unit test patterns for CLI applications
   - Integration testing approach
   - Test coverage targets

### Key Technical Decisions

#### Decision 1: CLI Interface Pattern
**Options Considered**:
- A) Interactive REPL (Read-Eval-Print Loop)
- B) Single-command execution (e.g., `todo add "task"`)
- C) Hybrid (REPL with command-line support)

**Decision**: Option A - Interactive REPL
**Rationale**:
- Better user experience for multiple operations in one session
- Aligns with "session-only" data retention model
- Simpler error recovery (user stays in application)
- Natural fit for in-memory storage (session lifecycle matches data lifecycle)

**Implementation**: Use Python's `cmd` module or custom input loop with command parsing

#### Decision 2: Task ID Strategy
**Options Considered**:
- A) Auto-incrementing integer (1, 2, 3...)
- B) UUID (universally unique identifier)
- C) Hash-based ID

**Decision**: Option A - Auto-incrementing integer
**Rationale**:
- User-friendly (easy to type and remember)
- Sufficient for in-memory, single-session use
- No collision risk in single-user, single-session context
- Aligns with user expectation for simple CLI tools

**Implementation**: Counter starting at 1, incremented on each add operation

#### Decision 3: Data Storage Structure
**Options Considered**:
- A) List of Task objects
- B) Dictionary with ID as key, Task as value
- C) Both (list for ordering, dict for fast lookup)

**Decision**: Option B - Dictionary with ID as key
**Rationale**:
- O(1) lookup for update, delete, complete operations
- Maintains insertion order (Python 3.7+)
- Simpler than maintaining two structures
- Sufficient performance for 100 tasks

**Implementation**: `tasks: dict[int, Task] = {}`

#### Decision 4: Command Parsing Approach
**Options Considered**:
- A) argparse with subcommands
- B) Custom string parsing
- C) cmd module with do_* methods

**Decision**: Option C - cmd module with do_* methods
**Rationale**:
- Built-in support for REPL pattern
- Clean command handler separation
- Built-in help system
- No external dependencies

**Implementation**: Extend `cmd.Cmd` class with `do_add`, `do_list`, etc.

#### Decision 5: Testing Strategy
**Options Considered**:
- A) Unit tests only
- B) Integration tests only
- C) Both unit and integration tests

**Decision**: Option C - Both unit and integration tests
**Rationale**:
- Unit tests verify individual components (models, services, validators)
- Integration tests verify end-to-end command flows
- Comprehensive coverage ensures reliability
- Supports refactoring with confidence

**Implementation**: pytest with separate unit/ and integration/ directories

### Technology Stack Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python 3.13+ | Specified in requirements, modern features |
| Package Manager | UV | Specified in requirements, fast and reliable |
| CLI Framework | cmd module | Built-in, REPL support, no dependencies |
| Data Model | dataclasses | Built-in, clean syntax, type hints |
| Testing | pytest | Industry standard, rich ecosystem |
| Code Quality | ruff | Fast linter/formatter, replaces multiple tools |

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Core Entities**:
- **Task**: ID (int), description (str), status (TaskStatus enum)
- **TaskStatus**: Enum with PENDING and COMPLETE values

### API Contracts

See [contracts/cli-interface.md](./contracts/cli-interface.md) for complete command specifications.

**Command Interface**:
- `add <description>` - Add new task
- `list` - Display all tasks
- `update <id> <description>` - Update task description
- `complete <id>` - Mark task as complete
- `delete <id>` - Delete task
- `help` - Show available commands
- `exit` - Exit application

### Module Responsibilities

#### models/task.py
- Define Task dataclass with id, description, status fields
- Define TaskStatus enum (PENDING, COMPLETE)
- Provide task validation logic (non-empty description)

#### services/task_service.py
- Maintain in-memory task storage (dictionary)
- Implement CRUD operations (add, get, get_all, update, delete)
- Implement status change operation (mark_complete)
- Handle ID generation (auto-increment)
- Raise domain exceptions for invalid operations

#### cli/commands.py
- Extend cmd.Cmd for REPL interface
- Implement command handlers (do_add, do_list, etc.)
- Parse command arguments
- Call task_service methods
- Handle exceptions and display results

#### cli/display.py
- Format task list output (table format)
- Format success/error messages
- Provide consistent user feedback
- Handle empty state messaging

#### utils/validators.py
- Validate task descriptions (non-empty, length limits)
- Validate task IDs (numeric, positive)
- Provide clear validation error messages

### Error Handling Strategy

**Error Categories**:
1. **Validation Errors**: Empty description, invalid ID format
2. **Not Found Errors**: Task ID doesn't exist
3. **State Errors**: Marking already-complete task as complete

**Handling Approach**:
- Custom exception classes (ValidationError, TaskNotFoundError)
- CLI layer catches exceptions and displays user-friendly messages
- No application crashes - all errors handled gracefully
- Clear error messages with actionable guidance

### Testing Strategy

**Unit Tests** (tests/unit/):
- test_task.py: Task model validation, status transitions
- test_task_service.py: CRUD operations, ID generation, error cases
- test_validators.py: Input validation logic
- test_display.py: Output formatting

**Integration Tests** (tests/integration/):
- test_cli_commands.py: End-to-end command execution, user workflows

**Coverage Target**: 90%+ line coverage

**Test Execution**: `pytest tests/ --cov=src --cov-report=term-missing`

## Implementation Phases

### Phase 0: Environment Setup ✅
- Initialize /phase-1 directory
- Set up UV project (pyproject.toml)
- Configure Python 3.13
- Install development dependencies (pytest, ruff)

### Phase 1: Core Domain Model
- Implement Task dataclass
- Implement TaskStatus enum
- Write unit tests for Task model

### Phase 2: Business Logic Layer
- Implement TaskService with in-memory storage
- Implement CRUD operations
- Write unit tests for TaskService

### Phase 3: Validation Layer
- Implement input validators
- Write unit tests for validators

### Phase 4: CLI Interface
- Implement command handlers
- Implement display formatting
- Write integration tests for CLI commands

### Phase 5: Integration & Polish
- End-to-end testing
- Error handling refinement
- User feedback improvements
- README documentation

### Phase 6: Verification
- Run full test suite
- Verify all acceptance criteria
- Performance testing (100 tasks)
- User acceptance testing

## Acceptance Criteria

### Functional Acceptance
- [ ] All 14 functional requirements (FR-001 to FR-014) implemented and verified
- [ ] All 4 user stories (P1-P4) with acceptance scenarios passing
- [ ] All edge cases handled gracefully

### Quality Acceptance
- [ ] 90%+ test coverage
- [ ] All tests passing
- [ ] No linter errors (ruff)
- [ ] Clean code principles followed (functions <20 lines, clear naming)

### Performance Acceptance
- [ ] All operations complete in <1 second with 100 tasks
- [ ] Memory usage reasonable (<50MB for 100 tasks)

### Documentation Acceptance
- [ ] README.md with setup and usage instructions
- [ ] Code comments for complex logic
- [ ] Docstrings for public functions

### Success Criteria Verification
- [ ] SC-001: Task addition in <5 seconds ✓
- [ ] SC-002: List view in <2 seconds ✓
- [ ] SC-003: 100% success rate for valid inputs ✓
- [ ] SC-004: Clear error messages for invalid inputs ✓
- [ ] SC-005: Intuitive first-time use ✓
- [ ] SC-006: Status changes immediately reflected ✓
- [ ] SC-007: 100 tasks without degradation ✓

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Python 3.13 not available on user system | High | Low | Document Python version requirement clearly, provide version check |
| UV package manager unfamiliar to users | Medium | Medium | Provide detailed setup instructions, include troubleshooting |
| REPL interface confusing for CLI users | Medium | Low | Provide clear help text, intuitive command names |
| Performance degradation with many tasks | Low | Low | Use efficient data structures (dict), performance test with 100+ tasks |
| Unicode handling in task descriptions | Low | Medium | Test with unicode characters, ensure UTF-8 encoding |

## Dependencies

### External Dependencies
- Python 3.13+ runtime
- UV package manager

### Development Dependencies
- pytest (testing framework)
- pytest-cov (coverage reporting)
- ruff (linting and formatting)

### Internal Dependencies
None - Phase 1 is self-contained

## Next Steps

1. Run `/sp.tasks` to generate dependency-ordered task list
2. Review and approve tasks.md
3. Run `/sp.implement` to execute implementation
4. Create ADRs for significant decisions (CLI pattern, data structure)
5. Commit and create PR with `/sp.git.commit_pr`

## Notes

- This plan establishes the foundation for future phases
- Phase 2 (Todo Full-Stack Web Application) will add persistence and web API while preserving CLI functionality
- Keep code modular to support future enhancements
- Document assumptions and design decisions for future reference
