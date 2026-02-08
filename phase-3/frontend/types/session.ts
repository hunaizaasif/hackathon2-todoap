// Session types (Better Auth)
export interface Session {
  id: string;
  user_id: string;
  expires_at: string;
  created_at: string;
}

// Session data exposed to frontend
export interface SessionData {
  user: {
    id: string;
    email: string;
    created_at: string;
  };
  expiresAt: string;
}
