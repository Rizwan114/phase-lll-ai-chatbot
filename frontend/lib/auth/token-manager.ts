export const tokenManager = {
  getAccessToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("access_token");
  },

  setAccessToken(token: string): void {
    localStorage.setItem("access_token", token);
  },

  removeAccessToken(): void {
    localStorage.removeItem("access_token");
  },

  getUserId(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("user_id");
  },

  setUserId(userId: string): void {
    localStorage.setItem("user_id", userId);
  },

  removeUserId(): void {
    localStorage.removeItem("user_id");
  },

  isTokenExpired(): boolean {
    const token = this.getAccessToken();
    if (!token) return true;
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  },

  clearAll(): void {
    this.removeAccessToken();
    this.removeUserId();
  },
};
