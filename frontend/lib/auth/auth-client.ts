import { tokenManager } from "./token-manager";
import { JWTClaims } from "./auth-types";

export const authClient = {
  getCurrentUserId(): string | null {
    const token = tokenManager.getAccessToken();
    if (!token) return null;
    try {
      const payload: JWTClaims = JSON.parse(atob(token.split(".")[1]));
      return payload.sub || payload.user_id || null;
    } catch {
      return null;
    }
  },

  isAuthenticated(): boolean {
    return !tokenManager.isTokenExpired() && !!tokenManager.getAccessToken();
  },

  getTokenClaims(): JWTClaims | null {
    const token = tokenManager.getAccessToken();
    if (!token) return null;
    try {
      return JSON.parse(atob(token.split(".")[1]));
    } catch {
      return null;
    }
  },
};
