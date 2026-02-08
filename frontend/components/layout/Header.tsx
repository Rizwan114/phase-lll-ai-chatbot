"use client";

import { useAuth } from "@/lib/auth/auth-context";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";

export function Header() {
  const { isAuthenticated, userId, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600">
            <svg
              className="h-4.5 w-4.5 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2.5}
                d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
              />
            </svg>
          </div>
          <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">
            Todo App
          </h1>
        </div>

        {isAuthenticated && (
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xs font-bold uppercase">
                {userId?.charAt(0) || "?"}
              </div>
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300 hidden sm:inline">
                {userId}
              </span>
            </div>
            <div className="w-px h-5 bg-gray-200 dark:bg-gray-700 hidden sm:block" />
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              Sign Out
            </Button>
          </div>
        )}
      </div>
    </header>
  );
}
