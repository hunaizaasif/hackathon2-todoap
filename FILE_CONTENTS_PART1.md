# Phase 2 - Complete File Contents for Copy-Paste

## 📋 How to Use This Guide

1. Open your Space: https://huggingface.co/spaces/Amber-Asif/todo-app-phase-2
2. Click "Files" → "Add file" → "Create a new file"
3. Type the filename (e.g., `Dockerfile`)
4. Copy content from below and paste
5. Click "Commit new file"
6. Repeat for all files

---

## 🔹 ROOT FILES

### File: Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY main.py .
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

EXPOSE 7860

# Run migrations and start server
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port 7860"]
```

---

### File: README.md

```markdown
---
title: Phase 2 Todo API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Phase 2 Todo API

A persistent, multi-user Todo API built with FastAPI, SQLModel, and PostgreSQL.

## Features

- ✅ User authentication with JWT tokens
- ✅ CRUD operations for tasks
- ✅ Multi-user support with user isolation
- ✅ PostgreSQL database with SQLModel ORM
- ✅ Database migrations with Alembic
- ✅ Comprehensive error handling
- ✅ Request logging and monitoring

## API Documentation

Once deployed, visit `/docs` for interactive API documentation (Swagger UI).

## Environment Variables

Configure these in your Hugging Face Space settings:

```
DATABASE_URL=postgresql://user:password@host:port/database
AUTH_SECRET_KEY=your-secret-key-here
DEBUG=false
```

## Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /tasks` - List all tasks (authenticated)
- `POST /tasks` - Create new task (authenticated)
- `GET /tasks/{id}` - Get task by ID (authenticated)
- `PUT /tasks/{id}` - Update task (authenticated)
- `DELETE /tasks/{id}` - Delete task (authenticated)

## Tech Stack

- FastAPI
- SQLModel
- PostgreSQL (Neon Serverless)
- Alembic
- Pydantic
- Python 3.13+
```

---

### File: pyproject.toml

```toml
[project]
name = "phase-2-todo-api"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.13"
dependencies = [
    "alembic>=1.18.3",
    "email-validator>=2.3.0",
    "fastapi>=0.128.1",
    "httpx>=0.28.1",
    "passlib[bcrypt]>=1.7.4",
    "psycopg2-binary>=2.9.11",
    "pydantic-settings>=2.12.0",
    "pytest>=9.0.2",
    "pytest-cov>=7.0.0",
    "python-jose[cryptography]>=3.5.0",
    "python-multipart>=0.0.22",
    "sqlmodel>=0.0.32",
    "uvicorn>=0.40.0",
]

[dependency-groups]
dev = [
    "httpx>=0.28.1",
    "pytest>=9.0.2",
    "pytest-asyncio>=1.3.0",
]
```

---

### File: alembic.ini

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

---

**Note**: For `main.py` and `uv.lock`, files are too large. I'll provide them in next message.

Continue to next section? (Y/N)
