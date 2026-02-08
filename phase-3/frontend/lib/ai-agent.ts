import OpenAI from "openai";

// Lazy initialization to avoid build-time errors
function getOpenAIClient() {
  return new OpenAI({
    apiKey: process.env.OPENAI_API_KEY || "dummy-key-for-build",
    baseURL: process.env.OPENAI_BASE_URL || "https://openrouter.ai/api/v1",
  });
}

export interface MCPTool {
  name: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, any>;
    required?: string[];
  };
}

// Fetch MCP tools from MCP server
export async function getMCPTools(): Promise<MCPTool[]> {
  try {
    const response = await fetch(
      `${process.env.MCP_SERVER_URL || "http://localhost:3001"}/tools`
    );
    const data = await response.json();
    return data.tools;
  } catch (error) {
    console.error("Failed to fetch MCP tools:", error);
    return [];
  }
}

// Execute MCP tool
export async function executeMCPTool(
  toolName: string,
  args: Record<string, any>,
  token?: string
): Promise<{ content: Array<{ type: string; text?: string }>; isError?: boolean }> {
  try {
    // Get token from localStorage if not provided
    const authToken = token || (typeof window !== 'undefined' ? localStorage.getItem("auth_token") : null);

    const response = await fetch(
      `${process.env.MCP_SERVER_URL || "http://localhost:3001"}/tools/execute`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(authToken && { Authorization: `Bearer ${authToken}` }),
        },
        body: JSON.stringify({
          name: toolName,
          arguments: args,
        }),
      }
    );

    return await response.json();
  } catch (error) {
    console.error("Failed to execute MCP tool:", error);
    return {
      content: [
        {
          type: "text",
          text: `Error executing tool: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
}

// Convert MCP tools to OpenAI function format
export function mcpToolsToOpenAIFunctions(mcpTools: MCPTool[]) {
  return mcpTools.map((tool) => ({
    type: "function" as const,
    function: {
      name: tool.name,
      description: tool.description,
      parameters: tool.inputSchema,
    },
  }));
}

// Create chat completion with tool calling
export async function createChatCompletion(
  messages: Array<{ role: string; content: string }>,
  tools: MCPTool[]
) {
  const openai = getOpenAIClient();
  const openaiTools = mcpToolsToOpenAIFunctions(tools);

  const response = await openai.chat.completions.create({
    model: "openai/gpt-3.5-turbo",
    messages: messages as any,
    tools: openaiTools,
    tool_choice: "auto",
  });

  return response;
}
