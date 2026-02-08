// Task types (from Phase 2)
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string;
  status: string; // "pending" | "in_progress" | "complete"
  created_at: string;
  updated_at: string;
}

// Task creation input (frontend)
export interface CreateTaskInput {
  title: string;
  description?: string;
}

// Task update input (frontend)
export interface UpdateTaskInput {
  title?: string;
  description?: string;
  status?: string;
}

// Task filters (frontend)
export interface TaskFilters {
  status?: string;
  search?: string;
  sortBy?: "created_at" | "updated_at" | "title";
  sortOrder?: "asc" | "desc";
}
