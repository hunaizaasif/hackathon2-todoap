import { Phase2Client } from "../client";
import { MCPToolCallResponse } from "../types";

export async function addTask(
  client: Phase2Client,
  args: { title: string; description?: string }
): Promise<MCPToolCallResponse> {
  try {
    const task = await client.createTask({
      title: args.title,
      description: args.description,
    });

    return {
      content: [
        {
          type: "text",
          text: `✓ Task created successfully: "${task.title}" (ID: ${task.id})`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `✗ Error creating task: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
}
