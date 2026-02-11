import { apiClient } from "./api-client";
import { ChatResponse, ChatHistoryResponse } from "./types";

export const chatService = {
  async sendMessage(
    userId: string,
    message: string,
    conversationId?: string
  ): Promise<ChatResponse> {
    return apiClient.post<ChatResponse>(`/api/${userId}/chat`, {
      message,
      conversation_id: conversationId,
    });
  },

  async getHistory(userId: string): Promise<ChatHistoryResponse> {
    return apiClient.get<ChatHistoryResponse>(`/api/${userId}/chat/history`);
  },
};
