# Phase 3: AI Agent & MCP Integration

Modern Next.js 15+ web frontend with AI-powered task management capabilities.

## Features

- 🎯 **Task Dashboard**: Visual task management interface
- 🔐 **Secure Authentication**: Better Auth with Neon PostgreSQL
- 🤖 **AI Chat Interface**: Natural language task management
- 🔧 **MCP Tools**: Model Context Protocol server for AI agent integration

## Tech Stack

- **Frontend**: Next.js 15+, React 19, TypeScript, Tailwind CSS, Shadcn UI
- **Authentication**: Better Auth
- **AI**: OpenAI Agents SDK
- **MCP Server**: TypeScript, MCP SDK
- **Database**: Neon Serverless PostgreSQL (shared with Phase 2)

## Prerequisites

- Node.js 18+
- npm/yarn/pnpm
- Phase 2 backend running on `http://localhost:8000`
- OpenAI API key
- Neon PostgreSQL database (from Phase 2)

## Quick Start

### 1. Install Dependencies

```bash
# Frontend
cd frontend
npm install

# MCP Server
cd ../mcp-server
npm install
```

### 2. Configure Environment Variables

```bash
# Frontend
cd frontend
cp .env.example .env.local
# Edit .env.local with your values

# MCP Server
cd ../mcp-server
cp .env.example .env
# Edit .env with your values
```

### 3. Database Setup

Run the Alembic migration to add Better Auth tables:

```bash
cd ../../phase-2
alembic upgrade head
```

### 4. Start Development Servers

**Terminal 1 - Phase 2 Backend** (if not already running):
```bash
cd phase-2
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - MCP Server**:
```bash
cd phase-3/mcp-server
npm run dev
```

**Terminal 3 - Next.js Frontend**:
```bash
cd phase-3/frontend
npm run dev
```

### 5. Access the Application

- Frontend: http://localhost:3000
- Phase 2 API: http://localhost:8000
- MCP Server: http://localhost:3001

## Project Structure

```
phase-3/
├── frontend/              # Next.js 15+ application
│   ├── app/              # App Router pages
│   ├── components/       # React components
│   ├── lib/             # Utilities and configurations
│   ├── hooks/           # Custom React hooks
│   └── types/           # TypeScript type definitions
├── mcp-server/          # MCP server (separate service)
│   └── src/
│       ├── index.ts     # MCP server entry point
│       ├── tools/       # MCP tool implementations
│       └── client.ts    # Phase 2 API client
└── tests/               # Test suites
    ├── e2e/            # End-to-end tests
    ├── integration/    # Integration tests
    └── unit/           # Unit tests
```

## Development

### Frontend Development

```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler
```

### MCP Server Development

```bash
cd mcp-server
npm run dev          # Start dev server
npm run build        # Build TypeScript
npm run start        # Start production server
```

## Testing

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Integration tests
npm run test:integration
```

## Environment Variables

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

## Troubleshooting

### Cannot connect to Phase 2 backend

1. Verify Phase 2 is running: `curl http://localhost:8000/api/health`
2. Check CORS configuration in Phase 2
3. Verify `NEXT_PUBLIC_PHASE2_API_URL` in `.env.local`

### Database connection failed

1. Verify `DATABASE_URL` is correct
2. Test connection: `psql $DATABASE_URL -c "SELECT 1"`
3. Ensure Better Auth migrations have run

### OpenAI API error

1. Verify `OPENAI_API_KEY` is set correctly
2. Check OpenAI account has credits
3. Verify rate limits: https://platform.openai.com/account/limits

### MCP Server not responding

1. Verify MCP server is running: `curl http://localhost:3001/health`
2. Check MCP server logs for errors
3. Verify `MCP_SERVER_URL` in frontend `.env.local`

## Documentation

- [Specification](../../specs/003-ai-agent-mcp/spec.md)
- [Implementation Plan](../../specs/003-ai-agent-mcp/plan.md)
- [Task List](../../specs/003-ai-agent-mcp/tasks.md)
- [Quickstart Guide](../../specs/003-ai-agent-mcp/quickstart.md)

## License

See repository root for license information.
