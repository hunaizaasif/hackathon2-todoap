"use client";

import { useState } from "react";
import { TaskList } from "@/components/dashboard/TaskList";
import { TaskForm } from "@/components/dashboard/TaskForm";
import { TaskFilters } from "@/components/dashboard/TaskFilters";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { useTasks } from "@/hooks/useTasks";

export default function DashboardPage() {
  const { tasks, isLoading, error, createTask, updateTask, deleteTask, fetchTasks } = useTasks();
  const [showForm, setShowForm] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [filter, setFilter] = useState<"all" | "pending" | "in_progress" | "complete">("all");

  const handleFilterChange = (newFilter: "all" | "pending" | "in_progress" | "complete") => {
    setFilter(newFilter);
    if (newFilter === "all") {
      fetchTasks();
    } else {
      fetchTasks({ status: newFilter });
    }
  };

  const handleCreateTask = async (input: { title: string; description?: string }) => {
    await createTask(input);
    setShowForm(false);
  };

  const handleTaskCreatedViaChat = () => {
    // Refresh task list when task is created via chat
    fetchTasks();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-indigo-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 dark:bg-purple-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-30 animate-float"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-pink-300 dark:bg-pink-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-30 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-indigo-300 dark:bg-indigo-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-30 animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      <div className="container mx-auto px-4 py-8 relative z-10">
        {/* Header with 3D effect */}
        <div className="mb-8 animate-slide-in-up">
          <h1 className="text-5xl font-bold mb-3 bg-gradient-to-r from-purple-600 via-pink-600 to-indigo-600 bg-clip-text text-transparent">
            Task Dashboard
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            ✨ Manage your tasks with AI-powered assistance
          </p>
        </div>

        {/* Actions Bar with glass effect */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 animate-slide-in-up" style={{ animationDelay: '0.1s' }}>
          <TaskFilters filter={filter} onFilterChange={handleFilterChange} />
          <div className="flex gap-3">
            <button
              onClick={() => setShowChat(!showChat)}
              className="px-5 py-2.5 glass-effect rounded-xl hover:scale-105 transform transition-all duration-200 font-medium text-gray-800 dark:text-white shadow-lg hover:shadow-xl"
            >
              💬 AI Chat
            </button>
            <button
              onClick={() => setShowForm(!showForm)}
              className="px-5 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:scale-105 transform transition-all duration-200 font-medium shadow-lg hover:shadow-xl"
            >
              {showForm ? "✕ Cancel" : "✨ New Task"}
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 glass-effect border-l-4 border-red-500 rounded-xl text-red-600 dark:text-red-400 animate-scale-in">
            ⚠️ {error}
          </div>
        )}

        {/* Task Form with animation */}
        {showForm && (
          <div className="mb-6 p-6 glass-effect rounded-2xl shadow-xl animate-scale-in">
            <h2 className="text-2xl font-semibold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Create New Task
            </h2>
            <TaskForm onSubmit={handleCreateTask} onCancel={() => setShowForm(false)} />
          </div>
        )}

        {/* Task List */}
        <TaskList
          tasks={tasks}
          onUpdate={updateTask}
          onDelete={deleteTask}
          isLoading={isLoading}
        />
      </div>

      {/* Chat Sidebar */}
      <ChatSidebar
        isOpen={showChat}
        onClose={() => setShowChat(false)}
        onTaskCreated={handleTaskCreatedViaChat}
      />
    </div>
  );
}
