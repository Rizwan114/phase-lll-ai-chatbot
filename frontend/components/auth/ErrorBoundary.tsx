"use client";

import React from "react";
import { Button } from "@/components/ui/Button";

interface Props {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class AuthErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
  };

  handleLogin = () => {
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      const isAuthError = this.state.error?.message
        ?.toLowerCase()
        .includes("auth");

      return (
        <div className="flex flex-col items-center justify-center min-h-[300px] p-8">
          <svg
            className="h-12 w-12 text-red-400 mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            {isAuthError ? "Authentication Error" : "Something went wrong"}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4 text-center">
            {this.state.error?.message || "An unexpected error occurred"}
          </p>
          <div className="flex gap-3">
            <Button variant="secondary" onClick={this.handleRetry}>
              Try Again
            </Button>
            {isAuthError && (
              <Button variant="primary" onClick={this.handleLogin}>
                Go to Login
              </Button>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
