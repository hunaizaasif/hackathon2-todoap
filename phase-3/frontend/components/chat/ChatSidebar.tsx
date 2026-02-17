"use client";

import { useState } from "react";
import { ChatHistory } from "./ChatHistory";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "@/types/chat";

interface ChatSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onTaskCreated?: () => void;
}

export function ChatSidebar({ isOpen, onClose, onTaskCreated }: ChatSidebarProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      role: "user",
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Get auth token from localStorage
      const authToken = localStorage.getItem("auth_token");

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(authToken && { Authorization: `Bearer ${authToken}` }),
        },
        body: JSON.stringify({
          message: content,
          conversationHistory: messages,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }

      const data = await response.json();

      // Add assistant message
      setMessages((prev) => [...prev, data.message]);

      // If a task was created, notify parent to refresh
      if (data.toolsExecuted?.includes("add_task") && onTaskCreated) {
        onTaskCreated();
      }
    } catch (error) {
      console.error("Failed to send message:", error);
      // Add error message
      const errorMessage: ChatMessage = {
        id: `msg_${Date.now()}`,
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 animate-scale-in"
        onClick={onClose}
      />

      {/* Sidebar */}
      <div className="fixed right-0 top-0 h-full w-full md:w-[450px] glass-effect border-l border-white/20 shadow-2xl z-50 flex flex-col animate-slide-in-up">
        {/* Header with gradient */}
        <div className="flex items-center justify-between p-5 border-b border-white/20 bg-gradient-to-r from-purple-600/20 to-pink-600/20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white text-xl shadow-lg">
              🤖
            </div>
            <div>
              <h2 className="text-lg font-bold text-gray-800 dark:text-white">AI Assistant</h2>
              <p className="text-xs text-gray-600 dark:text-gray-300">Powered by OpenRouter</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-full glass-effect hover:bg-red-500/20 transition-all duration-200 flex items-center justify-center text-gray-600 dark:text-gray-300 hover:text-red-500 hover:scale-110 transform"
          >
            ✕
          </button>
        </div>

        {/* Chat History */}
        <ChatHistory messages={messages} isLoading={isLoading} />

        {/* Chat Input */}
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </>
  );
}
