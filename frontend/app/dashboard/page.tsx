"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import { Header } from "@/components/layout/Header";
import { TaskList } from "@/components/tasks/TaskList";
import { ChatFab } from "@/components/chat/ChatFab";
import { Spinner } from "@/components/ui/Spinner";

export default function DashboardPage() {
  const { isAuthenticated, isLoading, userId } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const greeting = (() => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  })();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Header />
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 animate-slide-up">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {greeting}, {userId}
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Here&apos;s what you&apos;re working on today
          </p>
        </div>
        <TaskList />
      </main>
      <ChatFab />
    </div>
  );
}
