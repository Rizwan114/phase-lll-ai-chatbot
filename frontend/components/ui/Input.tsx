"use client";

import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({
  label,
  error,
  className = "",
  id,
  ...props
}: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, "-");

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5"
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`w-full px-4 py-2.5 border-2 rounded-xl text-sm transition-all duration-200 focus:outline-none focus:ring-0 ${
          error
            ? "border-red-400 focus:border-red-500 dark:border-red-500"
            : "border-gray-200 focus:border-blue-500 dark:border-gray-700 dark:focus:border-blue-500"
        } bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 hover:border-gray-300 dark:hover:border-gray-600 ${className}`}
        {...props}
      />
      {error && (
        <p className="mt-1.5 text-xs text-red-500 flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
}
