---
title: Phase 3 MCP Server
emoji: 🔧
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Phase 3 MCP Server

Model Context Protocol (MCP) server for AI-powered task management. This server provides tools for the AI agent to interact with the Phase 2 Todo API.

## Features

- 🔧 **MCP Tools**: 5 task management tools (add, list, get, update, delete)
- 🔐 **Authentication**: JWT token-based auth with Phase 2 API
- 🚀 **RESTful API**: Simple HTTP endpoints for tool execution
- ⚡ **Fast**: Built with Node.js and TypeScript

## Available Tools

1. **add_task** - Create a new task
2. **list_tasks** - List all tasks with optional filtering
3. **get_task** - Get details of a specific task
4. **update_task** - Update task title, description, or status
5. **delete_task** - Delete a task permanently

## API Endpoints

- `GET /health` - Health check
- `GET /tools` - List available MCP tools
- `POST /tools/execute` - Execute an MCP tool

## Environment Variables

Configure these in your Hugging Face Space settings:

```
PHASE2_API_URL=https://your-phase2-api.hf.space
PORT=7860
```

## Usage Example

```bash
# Health check
curl https://YOUR_SPACE.hf.space/health

# List available tools
curl https://YOUR_SPACE.hf.space/tools

# Execute a tool (requires auth token)
curl -X POST https://YOUR_SPACE.hf.space/tools/execute \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "list_tasks",
    "arguments": {
      "status": "pending",
      "limit": 10
    }
  }'
```

## Integration

This MCP server is designed to work with:
- **Phase 2 API**: Backend task management API
- **Phase 3 Frontend**: Next.js AI chat interface
- **OpenAI Agents**: AI agents that use MCP tools

## Tech Stack

- Node.js 18+
- TypeScript
- MCP SDK
- HTTP server (built-in)

## Documentation

For more information, see the [Phase 3 README](https://github.com/hunaizaasif/hackathon2-todoap/tree/main/phase-3).
