// Chat message types
export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system" | "tool";
  content: string;
  timestamp: string;
  tool_calls?: ToolCall[];
  tool_call_id?: string;
}

export interface ToolCall {
  id: string;
  type: "function";
  function: {
    name: string;
    arguments: string;
  };
}

// Chat conversation (stored in SessionStorage)
export interface ChatConversation {
  id: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

// Chat input from user
export interface ChatInput {
  message: string;
  conversationId?: string;
}

// Chat response to user
export interface ChatResponse {
  message: ChatMessage;
  conversationId: string;
  toolsExecuted?: string[];
}
