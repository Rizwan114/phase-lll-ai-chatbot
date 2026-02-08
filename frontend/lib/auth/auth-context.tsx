"use client";

import React, { createContext, useContext, useCallback, useSyncExternalStore } from "react";

interface AuthState {
  userId: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface AuthContextType extends AuthState {
  login: (userId: string, token: string) => void;
  signup: (userId: string, token: string) => void;
  logout: () => void;
  getToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Use a simple external store to track auth state from localStorage.
// This avoids calling setState inside useEffect (react-hooks/set-state-in-effect).
let authListeners: Array<() => void> = [];
let authSnapshot: AuthState = { userId: null, isAuthenticated: false, isLoading: true };

function readAuthFromStorage(): AuthState {
  if (typeof window === "undefined") {
    return { userId: null, isAuthenticated: false, isLoading: true };
  }
  const token = localStorage.getItem("access_token");
  const userId = localStorage.getItem("user_id");
  if (token && userId) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      const isExpired = payload.exp * 1000 < Date.now();
      if (isExpired) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user_id");
        return { userId: null, isAuthenticated: false, isLoading: false };
      }
      return { userId, isAuthenticated: true, isLoading: false };
    } catch {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user_id");
      return { userId: null, isAuthenticated: false, isLoading: false };
    }
  }
  return { userId: null, isAuthenticated: false, isLoading: false };
}

function emitAuthChange() {
  authSnapshot = readAuthFromStorage();
  for (const listener of authListeners) {
    listener();
  }
}

function subscribeAuth(listener: () => void) {
  authListeners.push(listener);
  return () => {
    authListeners = authListeners.filter((l) => l !== listener);
  };
}

function getAuthSnapshot() {
  return authSnapshot;
}

const SERVER_SNAPSHOT: AuthState = { userId: null, isAuthenticated: false, isLoading: true };

function getAuthServerSnapshot(): AuthState {
  return SERVER_SNAPSHOT;
}

// Initialize snapshot on client
if (typeof window !== "undefined") {
  authSnapshot = readAuthFromStorage();
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const state = useSyncExternalStore(subscribeAuth, getAuthSnapshot, getAuthServerSnapshot);

  const login = useCallback((userId: string, token: string) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("user_id", userId);
    emitAuthChange();
  }, []);

  const signup = useCallback((userId: string, token: string) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("user_id", userId);
    emitAuthChange();
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    emitAuthChange();
  }, []);

  const getToken = useCallback(() => {
    return localStorage.getItem("access_token");
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, signup, logout, getToken }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
