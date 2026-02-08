import { apiClient } from "./api-client";
import { Task, TaskCreateRequest, TaskUpdateRequest, TaskListResponse } from "./types";

export const taskService = {
  async getTasks(userId: string): Promise<TaskListResponse> {
    return apiClient.get<TaskListResponse>(`/api/${userId}/tasks`);
  },

  async getTask(userId: string, taskId: number): Promise<Task> {
    return apiClient.get<Task>(`/api/${userId}/tasks/${taskId}`);
  },

  async createTask(userId: string, data: TaskCreateRequest): Promise<Task> {
    return apiClient.post<Task>(`/api/${userId}/tasks`, data);
  },

  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdateRequest
  ): Promise<Task> {
    return apiClient.put<Task>(`/api/${userId}/tasks/${taskId}`, data);
  },

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return apiClient.delete(`/api/${userId}/tasks/${taskId}`);
  },

  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    return apiClient.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`);
  },
};
