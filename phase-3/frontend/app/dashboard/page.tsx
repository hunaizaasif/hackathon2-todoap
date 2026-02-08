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
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Task Dashboard</h1>
          <p className="text-muted-foreground">
            Manage your tasks with AI-powered assistance
          </p>
        </div>

        {/* Actions Bar */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <TaskFilters filter={filter} onFilterChange={handleFilterChange} />
          <div className="flex gap-2">
            <button
              onClick={() => setShowChat(!showChat)}
              className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/80 font-medium"
            >
              💬 AI Chat
            </button>
            <button
              onClick={() => setShowForm(!showForm)}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 font-medium"
            >
              {showForm ? "Cancel" : "+ New Task"}
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-destructive/10 text-destructive rounded-md">
            {error}
          </div>
        )}

        {/* Task Form */}
        {showForm && (
          <div className="mb-6 p-6 border rounded-lg bg-card">
            <h2 className="text-xl font-semibold mb-4">Create New Task</h2>
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
