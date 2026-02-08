"use client";

import { AuthProvider } from "@/lib/auth/auth-context";
import { AuthErrorBoundary } from "@/components/auth/ErrorBoundary";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthErrorBoundary>
      <AuthProvider>{children}</AuthProvider>
    </AuthErrorBoundary>
  );
}
