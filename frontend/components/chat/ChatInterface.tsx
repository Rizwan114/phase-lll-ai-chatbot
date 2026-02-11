"use client";

import { useState, useEffect, useCallback } from "react";
import { ChatMessage } from "@/lib/api/types";
import { chatService } from "@/lib/api/chat-service";
import { MessageList } from "./MessageList";
import { MessageInput } from "./MessageInput";

interface ChatInterfaceProps {
  userId: string;
}

export function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadHistory() {
      try {
        const history = await chatService.getHistory(userId);
        if (cancelled) return;
        if (history.conversation_id) {
          setConversationId(history.conversation_id);
        }
        setMessages(history.messages);
      } catch (err) {
        if (cancelled) return;
        console.error("Failed to load chat history:", err);
      }
    }

    loadHistory();
    return () => {
      cancelled = true;
    };
  }, [userId]);

  const handleSend = useCallback(
    async (message: string) => {
      setError(null);
      setIsLoading(true);

      const optimisticMsg: ChatMessage = {
        id: Date.now(),
        role: "user",
        content: message,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, optimisticMsg]);

      try {
        const response = await chatService.sendMessage(
          userId,
          message,
          conversationId ?? undefined
        );

        if (!conversationId) {
          setConversationId(response.conversation_id);
        }

        const assistantMsg: ChatMessage = {
          id: Date.now() + 1,
          role: "assistant",
          content: response.response,
          created_at: new Date().toISOString(),
          tool_calls: response.tool_calls,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } catch (err) {
        const errorMessage =
          err instanceof Error
            ? err.message
            : "I'm having trouble right now. Please try again.";
        setError(errorMessage);

        const errorMsg: ChatMessage = {
          id: Date.now() + 1,
          role: "assistant",
          content: errorMessage,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
      }
    },
    [userId, conversationId]
  );

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-white dark:bg-gray-950">
      {error && (
        <div className="px-4 py-2 bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}
      <MessageList messages={messages} />
      <MessageInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
}
