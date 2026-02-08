"use client";

import { useState } from "react";
import type { Task } from "@/lib/api/types";
import { Button } from "@/components/ui/Button";
import { TaskForm } from "./TaskForm";

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: number) => Promise<void>;
  onUpdate: (
    taskId: number,
    data: { title: string; description: string }
  ) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
}

export function TaskItem({ task, onToggle, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggle(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  const handleUpdate = async (data: {
    title: string;
    description: string;
  }) => {
    await onUpdate(task.id, data);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsDeleting(false);
    }
  };

  if (isEditing) {
    return (
      <div className="p-4 border-2 border-blue-200 dark:border-blue-800 rounded-xl bg-blue-50/30 dark:bg-blue-900/10 animate-scale-in">
        <TaskForm
          onSubmit={handleUpdate}
          onCancel={() => setIsEditing(false)}
          initialValues={{
            title: task.title,
            description: task.description || "",
          }}
          submitLabel="Save Changes"
        />
      </div>
    );
  }

  return (
    <div
      className={`group flex items-start gap-3 p-4 rounded-xl border transition-all duration-200 ${
        task.completed
          ? "bg-gray-50/50 dark:bg-gray-800/30 border-gray-100 dark:border-gray-800"
          : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-900 hover:shadow-sm"
      }`}
    >
      {/* Checkbox */}
      <button
        onClick={handleToggle}
        disabled={isToggling}
        className={`mt-0.5 flex-shrink-0 w-5 h-5 rounded-md border-2 transition-all duration-200 flex items-center justify-center cursor-pointer ${
          task.completed
            ? "bg-green-500 border-green-500 text-white scale-100"
            : "border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20"
        } ${isToggling ? "opacity-50" : ""}`}
        aria-label={task.completed ? "Mark incomplete" : "Mark complete"}
      >
        {task.completed && (
          <svg className="w-3 h-3 animate-checkmark" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p
          className={`text-sm font-medium leading-snug transition-all duration-200 ${
            task.completed
              ? "line-through text-gray-400 dark:text-gray-500"
              : "text-gray-900 dark:text-gray-100"
          }`}
        >
          {task.title}
        </p>
        {task.description && (
          <p
            className={`mt-0.5 text-xs leading-relaxed transition-all duration-200 ${
              task.completed
                ? "line-through text-gray-300 dark:text-gray-600"
                : "text-gray-500 dark:text-gray-400"
            }`}
          >
            {task.description}
          </p>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex-shrink-0">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsEditing(true)}
          aria-label="Edit task"
          className="!px-2 !py-1.5"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleDelete}
          isLoading={isDeleting}
          aria-label="Delete task"
          className="!px-2 !py-1.5 text-red-400 hover:text-red-600 hover:!bg-red-50 dark:hover:!bg-red-900/20"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </Button>
      </div>
    </div>
  );
}
