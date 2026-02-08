import { Phase2Client } from "../client";
import { MCPToolCallResponse } from "../types";

export async function listTasks(
  client: Phase2Client,
  args: { status?: string; limit?: number }
): Promise<MCPToolCallResponse> {
  try {
    const response = await client.getTasks({
      status: args.status,
    });

    const tasks = response.tasks.slice(0, args.limit || 50);

    if (tasks.length === 0) {
      return {
        content: [
          {
            type: "text",
            text: "No tasks found.",
          },
        ],
      };
    }

    const taskList = tasks
      .map(
        (task, index) =>
          `${index + 1}. [${task.status === "complete" ? "✓" : task.status === "in_progress" ? "→" : " "}] ${task.title}${
            task.description ? ` - ${task.description}` : ""
          } (ID: ${task.id}, Status: ${task.status})`
      )
      .join("\n");

    return {
      content: [
        {
          type: "text",
          text: `Found ${tasks.length} task(s):\n\n${taskList}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `✗ Error listing tasks: ${error instanceof Error ? error.message : "Unknown error"}`,
        },
      ],
      isError: true,
    };
  }
}
