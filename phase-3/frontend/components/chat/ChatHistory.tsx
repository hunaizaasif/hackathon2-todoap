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
      className="flex-1 overflow-y-auto p-4 space-y-2"
      style={{ maxHeight: "calc(100vh - 200px)" }}
    >
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
          <p className="text-lg font-medium">Start a conversation</p>
          <p className="text-sm mt-2">
            Try: "Add buy milk to my list" or "Show me my tasks"
          </p>
        </div>
      ) : (
        messages.map((message) => (
          <ChatMessageComponent key={message.id} message={message} />
        ))
      )}
      {isLoading && (
        <div className="flex justify-start mb-4">
          <div className="bg-muted text-foreground rounded-lg px-4 py-2">
            <div className="flex gap-1">
              <span className="animate-bounce">●</span>
              <span className="animate-bounce delay-100">●</span>
              <span className="animate-bounce delay-200">●</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
