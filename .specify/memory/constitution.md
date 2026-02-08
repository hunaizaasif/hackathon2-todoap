<!--
Sync Impact Report:
- Version: Initial → 1.0.0
- Type: MAJOR (Initial constitution establishment)
- Modified Principles: N/A (new constitution)
- Added Sections: All (Core Principles, Phase Management, Development Workflow, Governance)
- Removed Sections: N/A
- Templates Status:
  ✅ spec-template.md - Reviewed, compatible with phase-based structure
  ✅ plan-template.md - Reviewed, constitution check section aligns
  ✅ tasks-template.md - Reviewed, user story structure compatible
- Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Core Principles

### I. Phase Isolation

Each phase MUST reside in its own subdirectory and be treated as an independent deliverable. Work on Phase N+1 is PROHIBITED until Phase N is formally closed and verified against its acceptance criteria.

**Phase Structure**:
- `/phase-1`: CLI Todo (Python 3.13, UV, In-memory)
- `/phase-2`: Todo Full-Stack Web Application (FastAPI, SQLModel, Neon DB, Better Auth)
- `/phase-3`: AI Agent & MCP (OpenAI Agents SDK, Model Context Protocol, Next.js)
- `/phase-4`: Cloud-Native & Orchestration (Docker, Kubernetes, Helm, AIOps)
- `/phase-5`: Event-Driven AI (Kafka, Dapr, Pub/Sub, Audit Logs)

**Rationale**: Phase isolation prevents scope creep, ensures each phase delivers complete value, and maintains clear architectural boundaries as the system evolves from CLI to cloud-native.

### II. Spec-Driven Development (NON-NEGOTIABLE)

Every phase MUST follow the strict sequence: **Specify → Plan → Tasks → Implement**. No implementation work begins until specification and planning artifacts are complete and approved.

**Mandatory Sequence**:
1. **Specify** (`/sp.specify`): Create feature specification with user stories, requirements, and success criteria
2. **Plan** (`/sp.plan`): Design architecture, technical approach, and project structure
3. **Tasks** (`/sp.tasks`): Generate dependency-ordered, testable task list
4. **Implement** (`/sp.implement`): Execute tasks with verification at each step

**Rationale**: Spec-first development ensures shared understanding, reduces rework, enables parallel work, and provides clear acceptance criteria before code is written.

### III. Scope Discipline

Features and requirements MUST strictly adhere to the phase definitions in the project document. Scope additions, enhancements, or "improvements" beyond the defined phase scope are PROHIBITED without explicit approval and re-planning.

**Enforcement**:
- All feature requests must reference the phase document
- "Nice to have" features are deferred to future phases
- Refactoring is limited to what's necessary for the current phase
- Cross-phase dependencies must be explicitly documented and justified

**Rationale**: Scope discipline ensures phases remain deliverable, prevents feature creep, and maintains the evolutionary architecture vision of the project.

### IV. Protected Directories

The following directories are system-managed and MUST NOT be modified or deleted:
- `.specify/` - SpecKit Plus templates and scripts
- `.specifyplus/` - System configuration (if present)
- `.speckit/` - Legacy system files (if present)

**Rationale**: These directories contain the development workflow infrastructure. Modifying them can break the spec-driven development process and automation.

### V. Verification-First

Every task MUST be verified against the phase's acceptance criteria before being marked complete. Verification includes functional testing, integration testing, and alignment with the specification.

**Verification Requirements**:
- Each task includes explicit acceptance criteria
- Tests (when specified) must pass before task completion
- Phase completion requires validation of ALL acceptance criteria
- Documentation must be updated to reflect implemented functionality

**Rationale**: Verification-first ensures quality, prevents technical debt, and provides confidence that each phase delivers its promised value before moving forward.

### VI. Evolutionary Architecture

The system architecture MUST evolve incrementally across phases, with each phase building on the previous phase's foundation while maintaining backward compatibility where feasible.

**Evolution Path**:
- Phase 1: Establish core domain logic and CLI interface
- Phase 2 (Todo Full-Stack Web Application): Add persistence and web API without breaking CLI
- Phase 3: Layer AI capabilities on existing API
- Phase 4: Containerize and orchestrate existing services
- Phase 5: Add event-driven patterns to existing architecture

**Rationale**: Evolutionary architecture allows learning from each phase, reduces risk, and ensures each phase delivers working software rather than building everything at once.

## Phase Management

### Phase Lifecycle

Each phase follows a strict lifecycle:

1. **Planning**: Specification, architecture design, and task breakdown
2. **Implementation**: Execute tasks in dependency order
3. **Verification**: Validate against acceptance criteria
4. **Closure**: Document outcomes, create ADRs for significant decisions
5. **Approval**: Explicit sign-off before next phase begins

### Phase Boundaries

- Each phase has its own directory structure under `/phase-N/`
- Shared assets (if required) reside in `/shared/`
- Cross-phase dependencies must be minimized and explicitly documented
- Phase N+1 may read from Phase N but MUST NOT modify Phase N code

### Phase Closure Criteria

A phase is considered closed when:
- All tasks marked complete and verified
- All acceptance criteria met
- Documentation updated (README, quickstart, API docs)
- Architectural decisions recorded in ADRs
- User acceptance obtained

## Development Workflow

### Workflow Sequence

1. **Feature Request**: User describes desired functionality
2. **Specification** (`/sp.specify`): Create spec.md with user stories and requirements
3. **Clarification** (`/sp.clarify`): Resolve ambiguities through targeted questions
4. **Planning** (`/sp.plan`): Design architecture and create plan.md
5. **Task Generation** (`/sp.tasks`): Create dependency-ordered tasks.md
6. **Analysis** (`/sp.analyze`): Cross-artifact consistency check
7. **Implementation** (`/sp.implement`): Execute tasks with verification
8. **ADR Creation** (`/sp.adr`): Document significant architectural decisions
9. **Git Workflow** (`/sp.git.commit_pr`): Commit and create pull request

### Quality Gates

- **Specification Gate**: Requirements clear, testable, and approved
- **Planning Gate**: Architecture sound, constitution-compliant, dependencies identified
- **Task Gate**: Tasks atomic, testable, dependency-ordered
- **Implementation Gate**: Tests pass, acceptance criteria met, code reviewed
- **Phase Gate**: All phase acceptance criteria verified before closure

### Prompt History Records (PHR)

Every user interaction MUST be recorded as a PHR in `history/prompts/`:
- Constitution work → `history/prompts/constitution/`
- Feature work → `history/prompts/<feature-name>/`
- General work → `history/prompts/general/`

PHRs capture full context, decisions, and outcomes for traceability and learning.

## Technology Constraints

### Phase-Specific Technology Stack

Each phase has a defined technology stack that MUST be adhered to:

- **Phase 1**: Python 3.13, UV package manager, in-memory storage
- **Phase 2 (Todo Full-Stack Web Application)**: FastAPI, SQLModel, Neon DB (PostgreSQL), Better Auth
- **Phase 3**: OpenAI Agents SDK, Model Context Protocol (MCP), Next.js
- **Phase 4**: Docker, Kubernetes, Helm, AIOps tooling
- **Phase 5**: Apache Kafka, Dapr, Pub/Sub patterns, audit logging

### Technology Selection

- Technology choices MUST align with phase definitions
- Deviations require explicit justification and ADR
- Prefer standard, well-documented libraries over custom solutions
- Consider operational complexity in technology decisions

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines. All code reviews, pull requests, and architectural decisions MUST verify compliance with these principles.

### Amendment Process

1. Proposed amendments must be documented with rationale
2. Impact analysis on existing phases and templates required
3. Team review and approval needed
4. Version bump according to semantic versioning:
   - **MAJOR**: Backward-incompatible principle changes
   - **MINOR**: New principles or material expansions
   - **PATCH**: Clarifications, wording improvements
5. Update all dependent templates and documentation
6. Create ADR documenting the amendment

### Compliance Review

- All specifications must reference constitution principles
- All plans must include "Constitution Check" section
- All tasks must align with phase scope and principles
- All PRs must verify no protected directory modifications

### Complexity Justification

Any violation of constitution principles (e.g., scope expansion, phase boundary crossing, technology deviation) MUST be explicitly justified in planning documents with:
- Why the violation is necessary
- What simpler alternatives were considered
- What risks the violation introduces
- How the violation will be managed

**Version**: 1.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05
