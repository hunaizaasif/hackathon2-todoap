"use client";

import { ChatMessage } from "@/types/chat";

interface ChatMessageProps {
  message: ChatMessage;
}

export function ChatMessageComponent({ message }: ChatMessageProps) {
  const isUser = message.role === "user";
  const isSystem = message.role === "system";

  if (isSystem) {
    return (
      <div className="flex justify-center my-3">
        <div className="text-xs text-gray-500 dark:text-gray-400 glass-effect px-4 py-2 rounded-full">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4 animate-slide-in-up`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-lg ${
          isUser
            ? "bg-gradient-to-r from-purple-600 to-pink-600 text-white"
            : "glass-effect text-gray-800 dark:text-white border border-white/20"
        }`}
      >
        <div className="text-sm whitespace-pre-wrap break-words leading-relaxed">
          {message.content}
        </div>
        <div className={`text-xs mt-2 ${isUser ? "text-white/70" : "text-gray-500 dark:text-gray-400"}`}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}
