import { Phase2Client } from "../client";
import { MCPToolCallResponse } from "../types";

export async function deleteTask(
  client: Phase2Client,
  args: { task_id: number }
): Promise<MCPToolCallResponse> {
  try {
    await client.deleteTask(args.task_id);

    return {
      content: [
        {
          type: "text",
          text: `✓ Task deleted successfully (ID: ${args.task_id})`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `✗ Error deleting task: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
}
