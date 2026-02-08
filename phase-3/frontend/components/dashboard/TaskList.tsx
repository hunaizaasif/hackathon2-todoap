"use client";

import { Task } from "@/types/task";
import { TaskCard } from "./TaskCard";

interface TaskListProps {
  tasks: Task[];
  onUpdate: (id: number, updates: Partial<Task>) => Promise<Task>;
  onDelete: (id: number) => Promise<void>;
  isLoading?: boolean;
}

export function TaskList({ tasks, onUpdate, onDelete, isLoading }: TaskListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-muted-foreground">Loading tasks...</div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <p className="text-lg font-medium text-muted-foreground">No tasks yet</p>
        <p className="text-sm text-muted-foreground mt-2">
          Create your first task to get started
        </p>
      </div>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
