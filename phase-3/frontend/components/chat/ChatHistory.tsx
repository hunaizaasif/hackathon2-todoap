"use client";

import { ChatMessage } from "@/types/chat";
import { ChatMessageComponent } from "./ChatMessage";
import { useEffect, useRef } from "react";

interface ChatHistoryProps {
  messages: ChatMessage[];
  isLoading?: boolean;
}

export function ChatHistory({ messages, isLoading }: ChatHistoryProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto p-5 space-y-2"
      style={{ maxHeight: "calc(100vh - 200px)" }}
    >
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-center animate-scale-in">
          <div className="glass-effect rounded-3xl p-8 max-w-sm">
            <div className="text-6xl mb-4 animate-float">💬</div>
            <p className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
              Start a conversation
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
              Try asking me to:
            </p>
            <div className="mt-4 space-y-2 text-sm text-left">
              <div className="glass-effect px-3 py-2 rounded-lg text-gray-700 dark:text-gray-200">
                💡 "Add buy milk to my list"
              </div>
              <div className="glass-effect px-3 py-2 rounded-lg text-gray-700 dark:text-gray-200">
                📋 "Show me my tasks"
              </div>
              <div className="glass-effect px-3 py-2 rounded-lg text-gray-700 dark:text-gray-200">
                ✅ "Mark task 5 as complete"
              </div>
            </div>
          </div>
        </div>
      ) : (
        messages.map((message) => (
          <ChatMessageComponent key={message.id} message={message} />
        ))
      )}
      {isLoading && (
        <div className="flex justify-start mb-4 animate-scale-in">
          <div className="glass-effect text-gray-800 dark:text-white rounded-2xl px-5 py-3 border border-white/20">
            <div className="flex gap-2 items-center">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-purple-600 rounded-full animate-bounce"></span>
                <span className="w-2 h-2 bg-pink-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                <span className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
              </div>
              <span className="text-sm text-gray-600 dark:text-gray-300">AI is thinking...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
