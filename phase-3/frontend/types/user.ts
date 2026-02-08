// User types (from Phase 2)
export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

// Frontend-safe user type (excludes sensitive fields)
export interface UserProfile {
  id: string;
  email: string;
  created_at: string;
}
