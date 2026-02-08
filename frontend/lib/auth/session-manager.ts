import { tokenManager } from "./token-manager";

export interface SessionInfo {
  isAuthenticated: boolean;
  userId: string | null;
  tokenExpired: boolean;
}

export const sessionManager = {
  getSession(): SessionInfo {
    const token = tokenManager.getAccessToken();
    const userId = tokenManager.getUserId();

    if (!token || !userId) {
      return { isAuthenticated: false, userId: null, tokenExpired: false };
    }

    const expired = tokenManager.isTokenExpired();
    if (expired) {
      tokenManager.clearAll();
      return { isAuthenticated: false, userId: null, tokenExpired: true };
    }

    return { isAuthenticated: true, userId, tokenExpired: false };
  },

  createSession(userId: string, accessToken: string): void {
    tokenManager.setAccessToken(accessToken);
    tokenManager.setUserId(userId);
  },

  destroySession(): void {
    tokenManager.clearAll();
  },
};
