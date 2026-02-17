"use client";

import { CreateTaskInput } from "@/types/task";
import { useState } from "react";

interface TaskFormProps {
  onSubmit: (input: CreateTaskInput) => Promise<void>;
  onCancel?: () => void;
}

export function TaskForm({ onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Reset form on success
      setTitle("");
      setDescription("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label htmlFor="title" className="block text-sm font-semibold mb-2 text-gray-700 dark:text-gray-200">
          ✨ Task Title *
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="w-full px-4 py-3 glass-effect rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-200 text-gray-800 dark:text-white placeholder-gray-400"
          disabled={isSubmitting}
          maxLength={255}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-semibold mb-2 text-gray-700 dark:text-gray-200">
          📝 Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details about this task..."
          rows={4}
          className="w-full px-4 py-3 glass-effect rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none transition-all duration-200 text-gray-800 dark:text-white placeholder-gray-400"
          disabled={isSubmitting}
          maxLength={2000}
        />
      </div>

      {error && (
        <div className="text-sm text-red-600 dark:text-red-400 glass-effect px-4 py-3 rounded-xl border-l-4 border-red-500 animate-scale-in">
          ⚠️ {error}
        </div>
      )}

      <div className="flex gap-3 pt-2">
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex-1 px-5 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:scale-105 transform transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-lg"
        >
          {isSubmitting ? "⏳ Creating..." : "✨ Create Task"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-5 py-3 glass-effect rounded-xl hover:scale-105 transform transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold text-gray-700 dark:text-gray-200"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
