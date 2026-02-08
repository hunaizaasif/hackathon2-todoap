import { Phase2Client } from "../client";
import { MCPToolCallResponse } from "../types";

export async function updateTask(
  client: Phase2Client,
  args: {
    task_id: number;
    title?: string;
    description?: string;
    status?: string;
  }
): Promise<MCPToolCallResponse> {
  try {
    const task = await client.updateTask(args.task_id, {
      title: args.title,
      description: args.description,
      status: args.status,
    });

    const updates = [];
    if (args.title) updates.push(`title to "${args.title}"`);
    if (args.description !== undefined) updates.push(`description`);
    if (args.status !== undefined)
      updates.push(`status to ${args.status}`);

    return {
      content: [
        {
          type: "text",
          text: `✓ Task updated successfully: "${task.title}" - Updated ${updates.join(", ")}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `✗ Error updating task: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
}
