"use client";

import { Task } from "@/types/task";
import { useState } from "react";

interface TaskCardProps {
  task: Task;
  onUpdate: (id: number, updates: Partial<Task>) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
}

export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggleStatus = async () => {
    setIsUpdating(true);
    try {
      // Cycle through statuses: pending -> in_progress -> complete -> pending
      const nextStatus =
        task.status === "pending"
          ? "in_progress"
          : task.status === "in_progress"
          ? "complete"
          : "pending";
      await onUpdate(task.id, { status: nextStatus });
    } catch (error) {
      console.error("Failed to update task:", error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }
    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } catch (error) {
      console.error("Failed to delete task:", error);
      setIsDeleting(false);
    }
  };

  const getStatusBadge = () => {
    switch (task.status) {
      case "complete":
        return "bg-green-100 text-green-800";
      case "in_progress":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-yellow-100 text-yellow-800";
    }
  };

  const getStatusLabel = () => {
    switch (task.status) {
      case "complete":
        return "Completed";
      case "in_progress":
        return "In Progress";
      default:
        return "Pending";
    }
  };

  const getNextStatusLabel = () => {
    switch (task.status) {
      case "pending":
        return "Start";
      case "in_progress":
        return "Complete";
      default:
        return "Reset";
    }
  };

  return (
    <div className="border rounded-lg p-4 bg-card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <h3
            className={`font-medium text-lg ${
              task.status === "complete" ? "line-through text-muted-foreground" : ""
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
              {task.description}
            </p>
          )}
          <div className="flex items-center gap-2 mt-3">
            <span className={`text-xs px-2 py-1 rounded-full ${getStatusBadge()}`}>
              {getStatusLabel()}
            </span>
            <span className="text-xs text-muted-foreground">
              {new Date(task.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
      <div className="flex gap-2 mt-4">
        <button
          onClick={handleToggleStatus}
          disabled={isUpdating || isDeleting}
          className="flex-1 px-3 py-2 text-sm font-medium rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
        >
          {isUpdating ? "..." : getNextStatusLabel()}
        </button>
        <button
          onClick={handleDelete}
          disabled={isDeleting || isUpdating}
          className="px-3 py-2 text-sm font-medium rounded-md bg-destructive text-destructive-foreground hover:bg-destructive/90 disabled:opacity-50"
        >
          {isDeleting ? "..." : "Delete"}
        </button>
      </div>
    </div>
  );
}
