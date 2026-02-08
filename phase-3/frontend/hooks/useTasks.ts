"use client";

import { useState, useEffect, useCallback } from "react";
import { Task, CreateTaskInput, UpdateTaskInput } from "@/types/task";
import { apiClient } from "@/lib/api-client";
import { autoLogin } from "@/lib/auth";

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Auto-login on mount
  useEffect(() => {
    autoLogin().then((success) => {
      setIsAuthenticated(success);
      if (!success) {
        setError("Failed to authenticate. Please refresh the page.");
        setIsLoading(false);
      }
    });
  }, []);

  const fetchTasks = useCallback(async (filter?: { status?: string }) => {
    if (!isAuthenticated) return;

    setIsLoading(true);
    setError(null);
    try {
      const response = await apiClient.getTasks(filter);
      setTasks(response.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
      console.error("Failed to fetch tasks:", err);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  const createTask = useCallback(async (input: CreateTaskInput) => {
    try {
      const newTask = await apiClient.createTask(input);
      setTasks((prev) => [newTask, ...prev]);
      return newTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create task";
      setError(message);
      throw new Error(message);
    }
  }, []);

  const updateTask = useCallback(async (id: number, updates: UpdateTaskInput) => {
    try {
      const updatedTask = await apiClient.updateTask(id, updates);
      setTasks((prev) =>
        prev.map((task) => (task.id === id ? updatedTask : task))
      );
      return updatedTask;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update task";
      setError(message);
      throw new Error(message);
    }
  }, []);

  const deleteTask = useCallback(async (id: number) => {
    try {
      await apiClient.deleteTask(id);
      setTasks((prev) => prev.filter((task) => task.id !== id));
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete task";
      setError(message);
      throw new Error(message);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [fetchTasks, isAuthenticated]);

  return {
    tasks,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
  };
}
