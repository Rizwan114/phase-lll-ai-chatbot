"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/lib/auth/auth-context";
import { taskService } from "@/lib/api/task-service";
import type { Task } from "@/lib/api/types";
import { TaskItem } from "./TaskItem";
import { TaskForm } from "./TaskForm";
import { Spinner } from "@/components/ui/Spinner";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";

export function TaskList() {
  const { userId } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

  const fetchTasks = useCallback(async () => {
    if (!userId) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await taskService.getTasks(userId);
      setTasks(response.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreate = async (data: {
    title: string;
    description: string;
  }) => {
    if (!userId) return;
    const newTask = await taskService.createTask(userId, {
      title: data.title,
      description: data.description || undefined,
    });
    setTasks((prev) => [newTask, ...prev]);
    setShowForm(false);
  };

  const handleToggle = async (taskId: number) => {
    if (!userId) return;
    const updated = await taskService.toggleComplete(userId, taskId);
    setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
  };

  const handleUpdate = async (
    taskId: number,
    data: { title: string; description: string }
  ) => {
    if (!userId) return;
    const updated = await taskService.updateTask(userId, taskId, {
      title: data.title,
      description: data.description || undefined,
    });
    setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
  };

  const handleDelete = async (taskId: number) => {
    if (!userId) return;
    await taskService.deleteTask(userId, taskId);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  const filteredTasks = tasks.filter((task) => {
    if (filter === "active") return !task.completed;
    if (filter === "completed") return task.completed;
    return true;
  });

  const activeTasks = tasks.filter((t) => !t.completed).length;
  const completedTasks = tasks.filter((t) => t.completed).length;

  if (isLoading) {
    return (
      <div className="py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return <ErrorState message={error} onRetry={fetchTasks} />;
  }

  return (
    <div className="animate-slide-up">
      <Card>
        <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">
              Tasks
            </h2>
            {tasks.length > 0 && (
              <div className="flex items-center gap-3 mt-1">
                <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-2 py-0.5 rounded-full">
                  {activeTasks} active
                </span>
                <span className="text-xs font-medium text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-2 py-0.5 rounded-full">
                  {completedTasks} done
                </span>
              </div>
            )}
          </div>
          <Button
            onClick={() => setShowForm(!showForm)}
            size="sm"
            variant={showForm ? "secondary" : "primary"}
          >
            {showForm ? (
              "Cancel"
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                New Task
              </>
            )}
          </Button>
        </CardHeader>

        <CardContent className="space-y-4">
          {showForm && (
            <div className="p-4 bg-blue-50/50 dark:bg-blue-900/10 rounded-xl border border-blue-100 dark:border-blue-900/30 animate-slide-down">
              <TaskForm
                onSubmit={handleCreate}
                onCancel={() => setShowForm(false)}
              />
            </div>
          )}

          {/* Filter tabs */}
          {tasks.length > 0 && (
            <div className="flex gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-xl w-fit">
              {(["all", "active", "completed"] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 capitalize cursor-pointer ${
                    filter === f
                      ? "bg-white dark:bg-gray-700 shadow-sm text-gray-900 dark:text-gray-100"
                      : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
                  }`}
                >
                  {f}
                  {f === "all" && ` (${tasks.length})`}
                  {f === "active" && ` (${activeTasks})`}
                  {f === "completed" && ` (${completedTasks})`}
                </button>
              ))}
            </div>
          )}

          {/* Task items */}
          {filteredTasks.length === 0 ? (
            <EmptyState
              title={
                filter === "all" ? "No tasks yet" : `No ${filter} tasks`
              }
              description={
                filter === "all"
                  ? "Create your first task to get started"
                  : undefined
              }
              action={
                filter === "all" ? (
                  <Button onClick={() => setShowForm(true)}>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Create Task
                  </Button>
                ) : undefined
              }
            />
          ) : (
            <div className="space-y-2">
              {filteredTasks.map((task, index) => (
                <div
                  key={task.id}
                  className="animate-slide-up"
                  style={{ animationDelay: `${index * 0.03}s`, animationFillMode: "both" }}
                >
                  <TaskItem
                    task={task}
                    onToggle={handleToggle}
                    onUpdate={handleUpdate}
                    onDelete={handleDelete}
                  />
                </div>
              ))}
            </div>
          )}

          {/* Progress bar */}
          {tasks.length > 0 && (
            <div className="pt-2">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  Progress
                </span>
                <span className="text-xs font-semibold text-gray-700 dark:text-gray-300">
                  {tasks.length > 0
                    ? Math.round((completedTasks / tasks.length) * 100)
                    : 0}
                  %
                </span>
              </div>
              <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-500 ease-out"
                  style={{
                    width: `${
                      tasks.length > 0
                        ? (completedTasks / tasks.length) * 100
                        : 0
                    }%`,
                  }}
                />
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
