// MCP Tool types
export interface MCPTool {
  name: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, any>;
    required?: string[];
  };
}

// MCP tool execution request
export interface MCPToolCallRequest {
  name: string;
  arguments: Record<string, any>;
}

// MCP tool execution response
export interface MCPToolCallResponse {
  content: Array<{
    type: "text" | "image" | "resource";
    text?: string;
    data?: string;
    mimeType?: string;
  }>;
  isError?: boolean;
}

// Task types (from Phase 2)
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  status: string; // "pending" | "in_progress" | "complete"
  created_at: string;
  updated_at: string;
}
