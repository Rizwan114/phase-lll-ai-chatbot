export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface ApiError {
  error: string;
  message: string;
  timestamp?: string;
}

export interface AuthSession {
  userId: string;
  accessToken: string;
  expiresAt: number;
}
