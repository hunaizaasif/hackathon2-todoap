import { Task } from "./types";

export class Phase2Client {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setToken(token: string) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(this.token && { Authorization: `Bearer ${this.token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: response.statusText,
      }));
      throw new Error(error.detail || `API error: ${response.statusText}`);
    }

    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  async getTasks(filters?: {
    status?: string;
  }): Promise<{ tasks: Task[]; total: number }> {
    const params = new URLSearchParams();
    if (filters?.status !== undefined) {
      params.set("status", filters.status);
    }

    const queryString = params.toString();
    const tasks = await this.request<Task[]>(
      `/tasks${queryString ? `?${queryString}` : ""}`
    );
    return { tasks, total: tasks.length };
  }

  async getTask(id: number): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`);
  }

  async createTask(input: {
    title: string;
    description?: string;
  }): Promise<Task> {
    return this.request<Task>("/tasks", {
      method: "POST",
      body: JSON.stringify({
        title: input.title,
        description: input.description || "",
        status: "pending",
      }),
    });
  }

  async updateTask(
    id: number,
    input: { title?: string; description?: string; status?: string }
  ): Promise<Task> {
    return this.request<Task>(`/tasks/${id}`, {
      method: "PATCH",
      body: JSON.stringify(input),
    });
  }

  async deleteTask(id: number): Promise<void> {
    return this.request<void>(`/tasks/${id}`, {
      method: "DELETE",
    });
  }
}
