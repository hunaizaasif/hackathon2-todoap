import { Phase2Client } from "../client";
import { MCPToolCallResponse } from "../types";

export async function getTask(
  client: Phase2Client,
  args: { task_id: number }
): Promise<MCPToolCallResponse> {
  try {
    const task = await client.getTask(args.task_id);

    return {
      content: [
        {
          type: "text",
          text: `Task Details:
Title: ${task.title}
Description: ${task.description || "(none)"}
Status: ${task.status}
Created: ${new Date(task.created_at).toLocaleString()}
Updated: ${new Date(task.updated_at).toLocaleString()}
ID: ${task.id}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `✗ Error getting task: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
}
