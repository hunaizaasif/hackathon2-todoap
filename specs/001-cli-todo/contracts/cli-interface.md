# CLI Interface Contract: Phase 1 CLI Todo

**Feature**: 001-cli-todo | **Date**: 2026-02-05 | **Phase**: Design (Phase 1)

## Overview

This document defines the command-line interface contract for the Phase 1 CLI Todo application. It specifies the exact syntax, behavior, and output format for each command in the interactive REPL interface.

## Interface Type

**Pattern**: Interactive REPL (Read-Eval-Print Loop)
**Framework**: Python cmd module
**Prompt**: `todo> `

## Command Reference

### 1. add - Add New Task

**Syntax**:
```
add <description>
```

**Description**: Creates a new task with the given description and assigns it a unique ID.

**Arguments**:
- `<description>`: Task description text (1-500 characters, required)

**Behavior**:
1. Validate description is not empty
2. Validate description does not exceed 500 characters
3. Generate unique auto-incrementing ID
4. Create task with status PENDING
5. Store task in memory
6. Display success message with task ID

**Success Output**:
```
✓ Task added successfully (ID: 1)
```

**Error Cases**:

| Error | Condition | Output |
|-------|-----------|--------|
| Empty description | No description provided | `Error: Task description cannot be empty` |
| Too long | Description > 500 chars | `Error: Task description cannot exceed 500 characters (got {length})` |

**Examples**:
```
todo> add Buy groceries
✓ Task added successfully (ID: 1)

todo> add
Error: Task description cannot be empty

todo> add Write a very long description that exceeds the maximum allowed length...
Error: Task description cannot exceed 500 characters (got 523)
```

---

### 2. list - Display All Tasks

**Syntax**:
```
list
```

**Description**: Displays all tasks with their ID, description, and status in a formatted table.

**Arguments**: None

**Behavior**:
1. Retrieve all tasks from storage
2. Format as table with columns: ID, Description, Status
3. Display in insertion order (oldest first)
4. Show empty state message if no tasks exist

**Success Output** (with tasks):
```
ID  Description              Status
──────────────────────────────────────
1   Buy groceries            Pending
2   Write documentation      Complete
3   Review pull request      Pending
```

**Success Output** (empty state):
```
No tasks found. Use 'add <description>' to create a task.
```

**Error Cases**: None (always succeeds)

**Examples**:
```
todo> list
ID  Description              Status
──────────────────────────────────────
1   Buy groceries            Pending
2   Write documentation      Complete

todo> list
No tasks found. Use 'add <description>' to create a task.
```

---

### 3. update - Update Task Description

**Syntax**:
```
update <id> <new_description>
```

**Description**: Updates the description of an existing task.

**Arguments**:
- `<id>`: Task ID (positive integer, required)
- `<new_description>`: New task description (1-500 characters, required)

**Behavior**:
1. Validate ID format (positive integer)
2. Validate task exists
3. Validate new description is not empty
4. Validate new description does not exceed 500 characters
5. Update task description
6. Display success message

**Success Output**:
```
✓ Task 1 updated successfully
```

**Error Cases**:

| Error | Condition | Output |
|-------|-----------|--------|
| Invalid ID format | Non-numeric or negative | `Error: Task ID must be a positive integer` |
| Task not found | ID doesn't exist | `Error: Task with ID {id} not found` |
| Empty description | No new description | `Error: Task description cannot be empty` |
| Too long | Description > 500 chars | `Error: Task description cannot exceed 500 characters (got {length})` |

**Examples**:
```
todo> update 1 Buy groceries and cook dinner
✓ Task 1 updated successfully

todo> update 999 New description
Error: Task with ID 999 not found

todo> update abc New description
Error: Task ID must be a positive integer

todo> update 1
Error: Task description cannot be empty
```

---

### 4. complete - Mark Task as Complete

**Syntax**:
```
complete <id>
```

**Description**: Marks a task as complete by changing its status from PENDING to COMPLETE.

**Arguments**:
- `<id>`: Task ID (positive integer, required)

**Behavior**:
1. Validate ID format (positive integer)
2. Validate task exists
3. Change task status to COMPLETE
4. Display success message
5. Handle gracefully if already complete (idempotent operation)

**Success Output**:
```
✓ Task 1 marked as complete
```

**Success Output** (already complete):
```
✓ Task 1 is already complete
```

**Error Cases**:

| Error | Condition | Output |
|-------|-----------|--------|
| Invalid ID format | Non-numeric or negative | `Error: Task ID must be a positive integer` |
| Task not found | ID doesn't exist | `Error: Task with ID {id} not found` |

**Examples**:
```
todo> complete 1
✓ Task 1 marked as complete

todo> complete 1
✓ Task 1 is already complete

todo> complete 999
Error: Task with ID 999 not found

todo> complete abc
Error: Task ID must be a positive integer
```

---

### 5. delete - Delete Task

**Syntax**:
```
delete <id>
```

**Description**: Permanently removes a task from the list.

**Arguments**:
- `<id>`: Task ID (positive integer, required)

**Behavior**:
1. Validate ID format (positive integer)
2. Validate task exists
3. Remove task from storage
4. Display success message

**Success Output**:
```
✓ Task 1 deleted successfully
```

**Error Cases**:

| Error | Condition | Output |
|-------|-----------|--------|
| Invalid ID format | Non-numeric or negative | `Error: Task ID must be a positive integer` |
| Task not found | ID doesn't exist | `Error: Task with ID {id} not found` |

**Examples**:
```
todo> delete 1
✓ Task 1 deleted successfully

todo> delete 999
Error: Task with ID 999 not found

todo> delete abc
Error: Task ID must be a positive integer
```

---

### 6. help - Display Help Information

**Syntax**:
```
help [command]
```

**Description**: Displays help information for all commands or a specific command.

**Arguments**:
- `[command]`: Optional command name for detailed help

**Behavior**:
1. If no argument: Display list of all commands with brief descriptions
2. If command specified: Display detailed help for that command
3. If invalid command: Display error message

**Success Output** (no argument):
```
Available commands:
  add <description>       Add a new task
  list                    Display all tasks
  update <id> <desc>      Update task description
  complete <id>           Mark task as complete
  delete <id>             Delete a task
  help [command]          Show this help message
  exit                    Exit the application

Type 'help <command>' for detailed information about a command.
```

**Success Output** (specific command):
```
todo> help add

add <description>
    Add a new task with the given description.

    Arguments:
        description: Task description text (1-500 characters)

    Example:
        add Buy groceries
```

**Error Cases**:

| Error | Condition | Output |
|-------|-----------|--------|
| Unknown command | Command doesn't exist | `Error: Unknown command '{command}'. Type 'help' for available commands.` |

---

### 7. exit - Exit Application

**Syntax**:
```
exit
```

**Description**: Exits the application cleanly.

**Arguments**: None

**Behavior**:
1. Display goodbye message
2. Exit with status code 0

**Success Output**:
```
Goodbye!
```

**Error Cases**: None (always succeeds)

**Examples**:
```
todo> exit
Goodbye!
```

**Aliases**: `quit`, `q`, Ctrl+D (EOF)

---

## Output Formatting Standards

### Success Messages

**Format**: `✓ <message>`
**Color**: Green (if terminal supports colors)
**Examples**:
- `✓ Task added successfully (ID: 1)`
- `✓ Task 1 updated successfully`
- `✓ Task 1 marked as complete`

### Error Messages

**Format**: `Error: <message>`
**Color**: Red (if terminal supports colors)
**Examples**:
- `Error: Task description cannot be empty`
- `Error: Task with ID 999 not found`
- `Error: Task ID must be a positive integer`

### Table Format (list command)

**Structure**:
```
ID  Description              Status
──────────────────────────────────────
1   Buy groceries            Pending
2   Write documentation      Complete
```

**Column Widths**:
- ID: 4 characters (right-aligned)
- Description: 25 characters (left-aligned, truncated with "..." if longer)
- Status: 10 characters (left-aligned)

**Separator**: Unicode box-drawing character (─) or ASCII dash (-)

---

## Error Handling Principles

1. **Never Crash**: All errors caught and displayed as user-friendly messages
2. **Actionable Messages**: Tell user what went wrong and how to fix it
3. **Consistent Format**: All errors start with "Error: "
4. **Graceful Degradation**: Invalid commands show help, not stack traces
5. **Idempotent Operations**: Completing an already-complete task succeeds

---

## Input Parsing Rules

1. **Command**: First word after prompt (case-insensitive)
2. **Arguments**: Remaining text after command
3. **Whitespace**: Leading/trailing whitespace trimmed
4. **Empty Input**: Ignored (re-display prompt)
5. **Unknown Commands**: Display error and suggest 'help'

**Examples**:
```
"  add   Buy groceries  " → command="add", args="Buy groceries"
"LIST" → command="list", args=""
"" → ignored
"unknown" → Error: Unknown command 'unknown'. Type 'help' for available commands.
```

---

## Session Lifecycle

### Startup

1. Display welcome message
2. Display prompt
3. Wait for user input

**Welcome Message**:
```
Welcome to CLI Todo!
Type 'help' for available commands or 'exit' to quit.

todo>
```

### Runtime

1. Read user input
2. Parse command and arguments
3. Execute command
4. Display output
5. Return to prompt

### Shutdown

1. Display goodbye message
2. Exit with status code 0
3. All data lost (in-memory only)

---

## Exit Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 0 | Success | Normal exit via 'exit' command |
| 1 | Error | Unhandled exception (should not occur) |

---

## Future Extensions (Phase 2+ - Todo Full-Stack Web Application and beyond)

Potential command additions for future phases:

- `search <query>` - Search tasks by description
- `filter <status>` - Filter tasks by status
- `sort <field>` - Sort tasks by field
- `export <file>` - Export tasks to file
- `import <file>` - Import tasks from file

These are NOT implemented in Phase 1.

---

## Testing Contract

Each command must have:
1. Unit tests for command handler logic
2. Integration tests for end-to-end command execution
3. Error case tests for all error conditions
4. Edge case tests (empty input, very long input, special characters)

**Test Coverage Target**: 100% of command handlers

---

**Document Status**: Complete
**Last Updated**: 2026-02-05
**Contract Version**: 1.0.0
