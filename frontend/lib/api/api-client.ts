import { ApiError } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

class ApiClient {
  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };
    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...(options.headers || {}),
      },
    };

    const response = await fetch(url, config);

    if (response.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_id");
        window.location.href = "/login";
      }
      throw new Error("Authentication expired. Please log in again.");
    }

    if (response.status === 204) {
      return undefined as T;
    }

    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        error: "UNKNOWN",
        message: `Request failed with status ${response.status}`,
      }));
      throw new Error(error.message || "An unexpected error occurred");
    }

    return response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "GET" });
  }

  async post<T>(endpoint: string, body: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async put<T>(endpoint: string, body: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
    });
  }

  async delete(endpoint: string): Promise<void> {
    return this.request<void>(endpoint, { method: "DELETE" });
  }

  async patch<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    });
  }
}

export const apiClient = new ApiClient();
