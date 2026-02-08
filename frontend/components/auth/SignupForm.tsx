"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import { authService } from "@/lib/auth/auth-service";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card, CardContent } from "@/components/ui/Card";
import Link from "next/link";

export function SignupForm() {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { signup } = useAuth();
  const router = useRouter();

  const passwordStrength = (() => {
    if (password.length === 0) return null;
    if (password.length < 6) return { label: "Too short", color: "bg-red-500", width: "w-1/4" };
    if (password.length < 8) return { label: "Fair", color: "bg-yellow-500", width: "w-2/4" };
    if (password.length < 12) return { label: "Good", color: "bg-blue-500", width: "w-3/4" };
    return { label: "Strong", color: "bg-green-500", width: "w-full" };
  })();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!userId.trim()) {
      setError("User ID is required");
      return;
    }
    if (!password.trim()) {
      setError("Password is required");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setIsLoading(true);
    try {
      const response = await authService.signup(userId, password);
      signup(response.user_id, response.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto animate-scale-in">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-lg shadow-emerald-500/20 mb-4">
          <svg
            className="h-7 w-7 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          Create your account
        </h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Get started with managing your tasks
        </p>
      </div>

      <Card>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="flex items-center gap-2 p-3 text-sm text-red-700 bg-red-50 dark:bg-red-900/20 dark:text-red-400 rounded-xl border border-red-100 dark:border-red-900/30 animate-slide-down">
                <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01" />
                </svg>
                {error}
              </div>
            )}
            <Input
              label="User ID"
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Choose a user ID"
              autoComplete="username"
              required
            />
            <div>
              <div className="relative">
                <Input
                  label="Password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Create a password (min 6 chars)"
                  autoComplete="new-password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-[34px] text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <svg className="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                    </svg>
                  ) : (
                    <svg className="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
              {passwordStrength && (
                <div className="mt-2 space-y-1">
                  <div className="h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${passwordStrength.color} ${passwordStrength.width} rounded-full transition-all duration-300`}
                    />
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {passwordStrength.label}
                  </p>
                </div>
              )}
            </div>
            <Input
              label="Confirm Password"
              type={showPassword ? "text" : "password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              autoComplete="new-password"
              required
            />
            <Button
              type="submit"
              className="w-full"
              isLoading={isLoading}
              size="lg"
            >
              {isLoading ? "Creating account..." : "Create Account"}
            </Button>
          </form>
        </CardContent>
      </Card>

      <p className="text-sm text-center text-gray-500 dark:text-gray-400 mt-6">
        Already have an account?{" "}
        <Link
          href="/login"
          className="text-blue-600 hover:text-blue-700 font-semibold transition-colors"
        >
          Sign in
        </Link>
      </p>
    </div>
  );
}
