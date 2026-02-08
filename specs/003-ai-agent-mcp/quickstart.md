# Quickstart Guide: Phase 3 AI Agent & MCP Integration

**Feature**: Phase 3 AI Agent & MCP Integration
**Date**: 2026-02-06
**Target Time**: <30 minutes for complete local setup

## Overview

This guide walks you through setting up Phase 3 locally for development. By the end, you'll have:
- Next.js frontend running on `http://localhost:3000`
- MCP server running and accessible to the AI agent
- Better Auth configured with Phase 2 database
- Full integration with Phase 2 backend

## Prerequisites

### Required Software
- **Node.js**: 18+ ([Download](https://nodejs.org/))
- **npm/yarn/pnpm**: Latest version
- **Git**: For version control
- **Phase 2 Backend**: Must be running on `http://localhost:8000`

### Required Accounts
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Neon Database**: Access to Phase 2 database (already configured)

### Verify Prerequisites

```bash
# Check Node.js version (should be 18+)
node --version

# Check npm version
npm --version

# Verify Phase 2 backend is running
curl http://localhost:8000/api/health
# Should return: {"status": "healthy"}
```

## Step 1: Clone and Navigate

```bash
# Navigate to project root
cd /path/to/Hackathon-2

# Checkout feature branch
git checkout 003-ai-agent-mcp

# Navigate to Phase 3 directory
cd phase-3
```

## Step 2: Install Dependencies

### Frontend Dependencies

```bash
cd frontend

# Install dependencies
npm install

# Expected packages:
# - next@15+
# - react@18+
# - better-auth
# - openai
# - @modelcontextprotocol/sdk
# - tailwindcss
# - lucide-react
# - zod
# - (and more - see package.json)
```

### MCP Server Dependencies

```bash
cd ../mcp-server

# Install dependencies
npm install

# Expected packages:
# - @modelcontextprotocol/sdk
# - typescript
# - (and more - see package.json)
```

## Step 3: Configure Environment Variables

### Frontend Environment

Create `frontend/.env.local`:

```bash
cd ../frontend
cp .env.local.example .env.local
```

Edit `frontend/.env.local`:

```env
# Phase 2 Backend
NEXT_PUBLIC_PHASE2_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# Database (Neon PostgreSQL - from Phase 2)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# OpenAI
OPENAI_API_KEY=sk-proj-...your-key-here...

# MCP Server
MCP_SERVER_URL=http://localhost:3001
```

**Generate BETTER_AUTH_SECRET**:
```bash
# Generate a secure random secret
openssl rand -base64 32
```

**Get DATABASE_URL**:
```bash
# Copy from Phase 2 .env file
cat ../../phase-2/.env | grep DATABASE_URL
```

### MCP Server Environment

Create `mcp-server/.env`:

```bash
cd ../mcp-server
cp .env.example .env
```

Edit `mcp-server/.env`:

```env
# Phase 2 Backend
PHASE2_API_URL=http://localhost:8000

# Server Port
PORT=3001
```

## Step 4: Database Setup (Better Auth Tables)

Better Auth requires additional tables in the Phase 2 database. Create a migration:

```bash
cd ../../phase-2

# Create Alembic migration for Better Auth tables
alembic revision -m "add_better_auth_tables"
```

Edit the generated migration file in `phase-2/alembic/versions/`:

```python
"""add_better_auth_tables

Revision ID: <generated_id>
Revises: <previous_revision>
Create Date: 2026-02-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '<generated_id>'
down_revision = '<previous_revision>'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sessions_user_id', 'sessions', ['user_id'])

    # Create verification_tokens table
    op.create_table(
        'verification_tokens',
        sa.Column('identifier', sa.String(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('expires', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('identifier', 'token')
    )


def downgrade() -> None:
    op.drop_table('verification_tokens')
    op.drop_index('idx_sessions_user_id', 'sessions')
    op.drop_table('sessions')
```

Run the migration:

```bash
# Apply migration
alembic upgrade head

# Verify tables were created
psql $DATABASE_URL -c "\dt"
# Should show: users, tasks, sessions, verification_tokens
```

## Step 5: Initialize Shadcn UI

```bash
cd ../phase-3/frontend

# Initialize Shadcn UI
npx shadcn-ui@latest init

# Follow prompts:
# - Style: Default
# - Base color: Slate
# - CSS variables: Yes

# Install required components
npx shadcn-ui@latest add button card input textarea dialog dropdown-menu badge separator scroll-area
```

## Step 6: Start Development Servers

### Terminal 1: Phase 2 Backend (if not already running)

```bash
cd phase-2
source .venv/bin/activate  # or activate your virtual environment
uvicorn src.main:app --reload --port 8000
```

**Verify**: Visit `http://localhost:8000/docs` - should see FastAPI docs

### Terminal 2: MCP Server

```bash
cd phase-3/mcp-server
npm run dev

# Expected output:
# MCP Server running on port 3001
# Connected to Phase 2 API at http://localhost:8000
```

**Verify**:
```bash
curl http://localhost:3001/health
# Should return: {"status": "healthy", "tools": 5}
```

### Terminal 3: Next.js Frontend

```bash
cd phase-3/frontend
npm run dev

# Expected output:
# ▲ Next.js 15.x.x
# - Local:        http://localhost:3000
# - Ready in 2.5s
```

**Verify**: Visit `http://localhost:3000` - should see landing page

## Step 7: Verify Setup

### 1. Test Authentication

```bash
# Create a test user
curl -X POST http://localhost:3000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "name": "Test User"
  }'

# Expected response:
# {
#   "user": { "id": "...", "email": "test@example.com", ... },
#   "session": { "token": "...", "expiresAt": "..." }
# }
```

### 2. Test Phase 2 Integration

Visit `http://localhost:3000/login` and sign in with test credentials.

After login, you should:
- See the dashboard at `http://localhost:3000`
- Be able to create tasks via the UI
- See tasks fetched from Phase 2 backend

### 3. Test AI Chat

In the dashboard:
1. Open the chat sidebar
2. Type: "Create a task to buy milk"
3. AI should respond and create the task
4. Verify task appears in dashboard

### 4. Test MCP Tools

```bash
# Get MCP server token (from frontend session)
TOKEN="<your-jwt-token>"

# Test list_tasks tool
curl -X POST http://localhost:3001/tools/call \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_tasks",
    "arguments": {}
  }'

# Should return list of tasks
```

## Common Issues & Solutions

### Issue 1: "Cannot connect to Phase 2 backend"

**Symptoms**: Frontend shows "API Error" when loading tasks

**Solutions**:
```bash
# 1. Verify Phase 2 is running
curl http://localhost:8000/api/health

# 2. Check CORS configuration in Phase 2
# Edit phase-2/src/main.py and ensure:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 3. Restart Phase 2 backend
```

### Issue 2: "Database connection failed"

**Symptoms**: Better Auth errors, cannot sign up/sign in

**Solutions**:
```bash
# 1. Verify DATABASE_URL is correct
echo $DATABASE_URL

# 2. Test database connection
psql $DATABASE_URL -c "SELECT 1"

# 3. Verify migrations ran
cd phase-2
alembic current
# Should show latest revision

# 4. Check if sessions table exists
psql $DATABASE_URL -c "\dt sessions"
```

### Issue 3: "OpenAI API error"

**Symptoms**: Chat returns "AI service error"

**Solutions**:
```bash
# 1. Verify API key is set
echo $OPENAI_API_KEY

# 2. Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# 3. Check OpenAI account has credits
# Visit: https://platform.openai.com/account/billing

# 4. Verify rate limits
# Visit: https://platform.openai.com/account/limits
```

### Issue 4: "MCP Server not responding"

**Symptoms**: Chat works but tasks aren't created

**Solutions**:
```bash
# 1. Verify MCP server is running
curl http://localhost:3001/health

# 2. Check MCP server logs
cd phase-3/mcp-server
npm run dev
# Look for errors in output

# 3. Verify MCP_SERVER_URL in frontend .env.local
cat frontend/.env.local | grep MCP_SERVER_URL

# 4. Test MCP tools directly
curl -X POST http://localhost:3001/tools/list
```

### Issue 5: "Port already in use"

**Symptoms**: Cannot start server, "EADDRINUSE" error

**Solutions**:
```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or use different port
PORT=3002 npm run dev
```

## Development Workflow

### Making Changes

1. **Frontend Changes**:
   ```bash
   cd phase-3/frontend
   # Edit files in app/, components/, lib/, etc.
   # Hot reload is automatic
   ```

2. **MCP Server Changes**:
   ```bash
   cd phase-3/mcp-server
   # Edit files in src/
   # Restart server: Ctrl+C, then npm run dev
   ```

3. **Database Changes**:
   ```bash
   cd phase-2
   # Create migration
   alembic revision -m "description"
   # Edit migration file
   # Apply migration
   alembic upgrade head
   ```

### Running Tests

```bash
# Frontend unit tests
cd phase-3/frontend
npm run test

# Frontend e2e tests
npm run test:e2e

# MCP server tests
cd ../mcp-server
npm run test
```

### Debugging

**Frontend Debugging**:
- Use browser DevTools (F12)
- Check Network tab for API calls
- Check Console for errors
- Use React DevTools extension

**Backend Debugging**:
- Check terminal output for errors
- Use `console.log()` in API routes
- Check Phase 2 logs for API errors
- Use Postman/curl to test APIs directly

**Database Debugging**:
```bash
# Connect to database
psql $DATABASE_URL

# Check tables
\dt

# Query data
SELECT * FROM users;
SELECT * FROM tasks;
SELECT * FROM sessions;
```

## Next Steps

After completing setup:

1. **Explore the codebase**:
   - Read `phase-3/frontend/README.md`
   - Review component structure
   - Understand data flow

2. **Run tests**:
   - Execute test suites
   - Verify all tests pass
   - Add new tests as needed

3. **Start development**:
   - Pick a task from `specs/003-ai-agent-mcp/tasks.md`
   - Create a feature branch
   - Implement and test
   - Create PR

4. **Read documentation**:
   - Review `specs/003-ai-agent-mcp/spec.md`
   - Study `specs/003-ai-agent-mcp/plan.md`
   - Understand architecture decisions

## Useful Commands

```bash
# Frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler

# MCP Server
npm run dev          # Start dev server
npm run build        # Build TypeScript
npm run start        # Start production server

# Phase 2 Backend
uvicorn src.main:app --reload  # Start dev server
pytest                          # Run tests
alembic upgrade head           # Apply migrations
```

## Environment Variables Reference

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_PHASE2_API_URL` | Phase 2 backend URL | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | Secret for session encryption | `<32+ char random string>` |
| `BETTER_AUTH_URL` | Frontend URL | `http://localhost:3000` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-...` |
| `MCP_SERVER_URL` | MCP server URL | `http://localhost:3001` |

### MCP Server (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `PHASE2_API_URL` | Phase 2 backend URL | `http://localhost:8000` |
| `PORT` | MCP server port | `3001` |

## Support

If you encounter issues not covered in this guide:

1. Check the [GitHub Issues](https://github.com/your-repo/issues)
2. Review the specification: `specs/003-ai-agent-mcp/spec.md`
3. Check the plan: `specs/003-ai-agent-mcp/plan.md`
4. Ask in team chat or create a new issue

## Summary

✅ **Setup Complete** when:
- All three servers running (Phase 2, MCP, Frontend)
- Can sign up and sign in
- Can create tasks via dashboard
- Can create tasks via AI chat
- All tests passing

**Estimated Setup Time**: 20-30 minutes

**Next**: Run `/sp.tasks` to generate implementation tasks
