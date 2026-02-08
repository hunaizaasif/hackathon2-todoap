import dotenv from "dotenv";
import { Phase2Client } from "./client";
import { addTask } from "./tools/add-task";
import { listTasks } from "./tools/list-tasks";
import { getTask } from "./tools/get-task";
import { updateTask } from "./tools/update-task";
import { deleteTask } from "./tools/delete-task";
import { MCPToolCallRequest, MCPToolCallResponse } from "./types";

// Load environment variables
dotenv.config();

const PHASE2_API_URL = process.env.PHASE2_API_URL || "http://localhost:8000";
const PORT = process.env.PORT || 3001;

// Initialize Phase 2 client
const phase2Client = new Phase2Client(PHASE2_API_URL);

// MCP Tool definitions
export const MCP_TOOLS = [
  {
    name: "add_task",
    description: "Create a new task for the user",
    inputSchema: {
      type: "object" as const,
      properties: {
        title: {
          type: "string",
          description: "The task title",
        },
        description: {
          type: "string",
          description: "Optional task description",
        },
      },
      required: ["title"],
    },
  },
  {
    name: "list_tasks",
    description: "List all tasks for the user with optional filtering",
    inputSchema: {
      type: "object" as const,
      properties: {
        status: {
          type: "string",
          description: "Filter by status: pending, in_progress, or complete",
        },
        limit: {
          type: "number",
          description: "Maximum number of tasks to return (default: 50)",
        },
      },
    },
  },
  {
    name: "get_task",
    description: "Get details of a specific task by ID",
    inputSchema: {
      type: "object" as const,
      properties: {
        task_id: {
          type: "number",
          description: "The unique identifier of the task",
        },
      },
      required: ["task_id"],
    },
  },
  {
    name: "update_task",
    description: "Update an existing task's title, description, or status",
    inputSchema: {
      type: "object" as const,
      properties: {
        task_id: {
          type: "number",
          description: "The unique identifier of the task to update",
        },
        title: {
          type: "string",
          description: "New task title",
        },
        description: {
          type: "string",
          description: "New task description",
        },
        status: {
          type: "string",
          description: "New status: pending, in_progress, or complete",
        },
      },
      required: ["task_id"],
    },
  },
  {
    name: "delete_task",
    description: "Permanently delete a task",
    inputSchema: {
      type: "object" as const,
      properties: {
        task_id: {
          type: "number",
          description: "The unique identifier of the task to delete",
        },
      },
      required: ["task_id"],
    },
  },
];

// Execute MCP tool
export async function executeTool(
  request: MCPToolCallRequest,
  token?: string
): Promise<MCPToolCallResponse> {
  // Set auth token if provided
  if (token) {
    phase2Client.setToken(token);
  }

  const { name, arguments: args } = request;

  switch (name) {
    case "add_task":
      return addTask(phase2Client, args);
    case "list_tasks":
      return listTasks(phase2Client, args);
    case "get_task":
      return getTask(phase2Client, args);
    case "update_task":
      return updateTask(phase2Client, args);
    case "delete_task":
      return deleteTask(phase2Client, args);
    default:
      return {
        content: [
          {
            type: "text",
            text: `Unknown tool: ${name}`,
          },
        ],
        isError: true,
      };
  }
}

// Simple HTTP server for MCP
if (require.main === module) {
  const http = require("http");

  const server = http.createServer(
    async (req: any, res: any) => {
      // CORS headers
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

      if (req.method === "OPTIONS") {
        res.writeHead(200);
        res.end();
        return;
      }

      // Health check
      if (req.url === "/health" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ status: "healthy", tools: MCP_TOOLS.length }));
        return;
      }

      // List tools
      if (req.url === "/tools" && req.method === "GET") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ tools: MCP_TOOLS }));
        return;
      }

      // Execute tool
      if (req.url === "/tools/execute" && req.method === "POST") {
        let body = "";
        req.on("data", (chunk: any) => {
          body += chunk.toString();
        });

        req.on("end", async () => {
          try {
            const request = JSON.parse(body);
            const token = req.headers.authorization?.replace("Bearer ", "");
            const result = await executeTool(request, token);

            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify(result));
          } catch (error) {
            res.writeHead(500, { "Content-Type": "application/json" });
            res.end(
              JSON.stringify({
                content: [
                  {
                    type: "text",
                    text: `Server error: ${error instanceof Error ? error.message : "Unknown error"}`,
                  },
                ],
                isError: true,
              })
            );
          }
        });
        return;
      }

      // 404
      res.writeHead(404, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Not found" }));
    }
  );

  server.listen(PORT, () => {
    console.log(`MCP Server running on http://localhost:${PORT}`);
    console.log(`Available tools: ${MCP_TOOLS.length}`);
  });
}
