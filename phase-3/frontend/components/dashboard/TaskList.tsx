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
      <div className="flex flex-col items-center justify-center py-16">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-purple-200 dark:border-purple-800 rounded-full"></div>
          <div className="w-16 h-16 border-4 border-purple-600 border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
        </div>
        <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">Loading your tasks...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 animate-scale-in">
        <div className="glass-effect rounded-3xl p-12 text-center max-w-md">
          <div className="text-6xl mb-4 animate-float">📝</div>
          <p className="text-xl font-semibold text-gray-800 dark:text-white mb-2">
            No tasks yet
          </p>
          <p className="text-gray-600 dark:text-gray-300">
            Create your first task to get started on your journey to productivity!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          <TaskCard
            task={task}
            onUpdate={onUpdate}
            onDelete={onDelete}
          />
        </div>
      ))}
    </div>
  );
}
