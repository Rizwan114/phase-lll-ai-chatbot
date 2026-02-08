const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

interface AuthResponse {
  access_token: string;
  user_id: string;
  token_type: string;
}

export const authService = {
  async login(userId: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        message: "Login failed",
      }));
      throw new Error(error.message || error.detail || "Login failed");
    }

    return response.json();
  },

  async signup(userId: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        message: "Signup failed",
      }));
      throw new Error(error.message || error.detail || "Signup failed");
    }

    return response.json();
  },

  isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  },

  getTokenUserId(token: string): string | null {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.sub || payload.user_id || null;
    } catch {
      return null;
    }
  },
};
