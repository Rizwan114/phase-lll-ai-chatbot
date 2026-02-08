"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import { Spinner } from "@/components/ui/Spinner";
import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function Home() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push("/dashboard");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/40 dark:from-gray-950 dark:via-gray-950 dark:to-gray-900">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-400/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-400/10 rounded-full blur-3xl" />
      </div>

      <div className="relative text-center max-w-lg animate-slide-up">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-xl shadow-blue-500/20 mb-8 animate-float">
          <svg
            className="h-10 w-10 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
        </div>

        {/* Heading */}
        <h1 className="text-5xl font-extrabold tracking-tight mb-4">
          <span className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 dark:from-white dark:via-gray-100 dark:to-white bg-clip-text text-transparent">
            Todo App
          </span>
        </h1>

        {/* Subheading */}
        <p className="text-lg text-gray-500 dark:text-gray-400 mb-10 leading-relaxed max-w-md mx-auto">
          Stay organized and get things done. A clean, fast task manager built for focus.
        </p>

        {/* CTA Buttons */}
        <div className="flex gap-3 justify-center">
          <Link href="/login">
            <Button size="lg">
              Sign In
            </Button>
          </Link>
          <Link href="/signup">
            <Button variant="secondary" size="lg">
              Create Account
            </Button>
          </Link>
        </div>

        {/* Feature pills */}
        <div className="flex flex-wrap gap-2 justify-center mt-12">
          {["Fast & Lightweight", "Secure Auth", "Real-time Sync"].map(
            (feature) => (
              <span
                key={feature}
                className="px-3 py-1.5 text-xs font-medium text-gray-500 dark:text-gray-400 bg-white/70 dark:bg-gray-800/70 border border-gray-200 dark:border-gray-700 rounded-full backdrop-blur-sm"
              >
                {feature}
              </span>
            )
          )}
        </div>
      </div>
    </div>
  );
}
