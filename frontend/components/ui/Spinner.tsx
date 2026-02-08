"use client";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function Spinner({ size = "md", className = "" }: SpinnerProps) {
  const sizes = {
    sm: "h-4 w-4 border-2",
    md: "h-8 w-8 border-[3px]",
    lg: "h-12 w-12 border-[3px]",
  };

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div
        className={`${sizes[size]} rounded-full border-gray-200 border-t-blue-600 animate-spin dark:border-gray-700 dark:border-t-blue-500`}
      />
    </div>
  );
}
