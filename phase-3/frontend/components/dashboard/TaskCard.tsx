"use client";

import { Task } from "@/types/task";
import { useState } from "react";

interface TaskCardProps {
  task: Task;
  onUpdate: (id: number, updates: Partial<Task>) => Promise<Task>;
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
        return "bg-gradient-to-r from-green-400 to-emerald-500 text-white shadow-lg";
      case "in_progress":
        return "bg-gradient-to-r from-blue-400 to-cyan-500 text-white shadow-lg";
      default:
        return "bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-lg";
    }
  };

  const getStatusLabel = () => {
    switch (task.status) {
      case "complete":
        return "✓ Completed";
      case "in_progress":
        return "⚡ In Progress";
      default:
        return "⏳ Pending";
    }
  };

  const getNextStatusLabel = () => {
    switch (task.status) {
      case "pending":
        return "▶ Start";
      case "in_progress":
        return "✓ Complete";
      default:
        return "↻ Reset";
    }
  };

  return (
    <div className="card-3d glass-effect rounded-2xl p-5 shadow-xl hover:shadow-2xl transition-all duration-300 animate-scale-in border border-white/20">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <h3
            className={`font-semibold text-lg mb-2 ${
              task.status === "complete"
                ? "line-through text-gray-500 dark:text-gray-400"
                : "text-gray-800 dark:text-white"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-gray-600 dark:text-gray-300 mt-1 line-clamp-2 leading-relaxed">
              {task.description}
            </p>
          )}
          <div className="flex items-center gap-2 mt-4">
            <span className={`text-xs px-3 py-1.5 rounded-full font-medium ${getStatusBadge()}`}>
              {getStatusLabel()}
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
              📅 {new Date(task.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
      <div className="flex gap-2 mt-5">
        <button
          onClick={handleToggleStatus}
          disabled={isUpdating || isDeleting}
          className="flex-1 px-4 py-2.5 text-sm font-medium rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:scale-105 transform transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          {isUpdating ? "⏳ Updating..." : getNextStatusLabel()}
        </button>
        <button
          onClick={handleDelete}
          disabled={isDeleting || isUpdating}
          className="px-4 py-2.5 text-sm font-medium rounded-xl bg-gradient-to-r from-red-500 to-pink-500 text-white hover:scale-105 transform transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          {isDeleting ? "⏳" : "🗑️"}
        </button>
      </div>
    </div>
  );
}
