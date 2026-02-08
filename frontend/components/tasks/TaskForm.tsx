"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface TaskFormProps {
  onSubmit: (data: { title: string; description: string }) => Promise<void>;
  onCancel?: () => void;
  initialValues?: { title: string; description: string };
  submitLabel?: string;
}

export function TaskForm({
  onSubmit,
  onCancel,
  initialValues,
  submitLabel = "Add Task",
}: TaskFormProps) {
  const [title, setTitle] = useState(initialValues?.title || "");
  const [description, setDescription] = useState(
    initialValues?.description || ""
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    setIsLoading(true);
    try {
      await onSubmit({ title: title.trim(), description: description.trim() });
      if (!initialValues) {
        setTitle("");
        setDescription("");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      {error && (
        <div className="flex items-center gap-2 p-2.5 text-xs text-red-700 bg-red-50 dark:bg-red-900/20 dark:text-red-400 rounded-lg border border-red-100 dark:border-red-900/30 animate-slide-down">
          <svg className="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01" />
          </svg>
          {error}
        </div>
      )}
      <Input
        placeholder="What needs to be done?"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        autoFocus
        required
      />
      <Input
        placeholder="Add a description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <div className="flex gap-2 justify-end pt-1">
        {onCancel && (
          <Button type="button" variant="ghost" size="sm" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" isLoading={isLoading} size="sm">
          {isLoading ? "Saving..." : submitLabel}
        </Button>
      </div>
    </form>
  );
}
