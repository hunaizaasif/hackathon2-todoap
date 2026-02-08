import { NextRequest, NextResponse } from "next/server";
import {
  createChatCompletion,
  getMCPTools,
  executeMCPTool,
} from "@/lib/ai-agent";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, conversationHistory = [] } = body;

    if (!message || typeof message !== "string") {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    // Get auth token from request headers
    const authToken = request.headers.get("authorization")?.replace("Bearer ", "");

    // Get MCP tools
    const mcpTools = await getMCPTools();

    // Build messages array
    const messages = [
      {
        role: "system",
        content: `You are a helpful AI assistant for task management. You can help users create, list, update, and delete tasks using natural language commands.

Available tools:
- add_task: Create a new task
- list_tasks: List all tasks (optionally filter by completed status)
- get_task: Get details of a specific task
- update_task: Update a task's title, description, or completion status
- delete_task: Delete a task

Be friendly, concise, and helpful. When users ask to create tasks, extract the task title and description from their message. When they ask about their tasks, use list_tasks. When they want to mark tasks as complete or update them, use update_task.`,
      },
      ...conversationHistory.slice(-10), // Last 10 messages for context
      {
        role: "user",
        content: message,
      },
    ];

    // Create chat completion
    const response = await createChatCompletion(messages, mcpTools);
    const assistantMessage = response.choices[0].message;

    // Handle tool calls
    if (assistantMessage.tool_calls && assistantMessage.tool_calls.length > 0) {
      const toolResults = [];

      for (const toolCall of assistantMessage.tool_calls) {
        const toolName = toolCall.function.name;
        const toolArgs = JSON.parse(toolCall.function.arguments);

        // Execute MCP tool with auth token
        const result = await executeMCPTool(toolName, toolArgs, authToken);

        toolResults.push({
          tool_call_id: toolCall.id,
          role: "tool",
          name: toolName,
          content: result.content[0]?.text || "Tool executed",
        });
      }

      // Get final response with tool results
      const finalMessages = [
        ...messages,
        {
          role: "assistant",
          content: assistantMessage.content || "",
          tool_calls: assistantMessage.tool_calls,
        },
        ...toolResults,
      ];

      const finalResponse = await createChatCompletion(
        finalMessages as any,
        mcpTools
      );

      return NextResponse.json({
        message: {
          id: `msg_${Date.now()}`,
          role: "assistant",
          content: finalResponse.choices[0].message.content || "Task completed.",
          timestamp: new Date().toISOString(),
          tool_calls: assistantMessage.tool_calls,
        },
        conversationId: `conv_${Date.now()}`,
        toolsExecuted: assistantMessage.tool_calls.map((tc) => tc.function.name),
      });
    }

    // No tool calls, return direct response
    return NextResponse.json({
      message: {
        id: `msg_${Date.now()}`,
        role: "assistant",
        content: assistantMessage.content || "I'm here to help with your tasks!",
        timestamp: new Date().toISOString(),
      },
      conversationId: `conv_${Date.now()}`,
    });
  } catch (error) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      {
        error: "Failed to process chat message",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}
