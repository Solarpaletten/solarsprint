// PROMPT_FRONTEND_01_C.md
// PURPOSE: Implement Login Page with localStorage auth
// VERSION: 2.0 — Fixed: save userId to localStorage after login

ROLE: SENIOR FRONTEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack: Next.js 14 (App Router), TypeScript, React 18, Tailwind CSS

TARGET FILE: app/(auth)/login/page.tsx

TASK:
Create Login Page with email/password form that saves auth to localStorage.

BACKEND API CONTRACT:
POST /api/auth/login
Request: { email: string, password: string }
Response: { id: string, email: string, tenantId: string }

CRITICAL: After successful login, MUST save userId to localStorage!
This is required for authenticated API calls.

REQUIRED TYPE DEFINITIONS:
```typescript
type LoginFormData = {
  email: string;
  password: string;
};

type LoginState = {
  isLoading: boolean;
  error: string | null;
};
```

FUNCTIONAL REQUIREMENTS:
1. 'use client' directive (Client Component)
2. Import useState from 'react'
3. Import useRouter from 'next/navigation'
4. Import Link from 'next/link'
5. Form with 2 fields: Email, Password
6. handleSubmit:
   - POST to /api/auth/login
   - Body: { email, password }
   - On success: 
     * SAVE userId: localStorage.setItem('userId', data.id)
     * SAVE tenantId: localStorage.setItem('tenantId', data.tenantId)
     * Redirect to /dashboard
   - On error: show error message
7. Loading state: "Signing in..."
8. Link to /signup for new users

COMPLETE CODE STRUCTURE:
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

type LoginFormData = {
  email: string;
  password: string;
};

type LoginState = {
  isLoading: boolean;
  error: string | null;
};

export default function LoginPage() {
  const router = useRouter();

  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: '',
  });

  const [state, setState] = useState<LoginState>({
    isLoading: false,
    error: null,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setState({ isLoading: true, error: null });

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      // CRITICAL: Save auth data to localStorage
      localStorage.setItem('userId', data.id);
      localStorage.setItem('tenantId', data.tenantId);

      router.push('/dashboard');
    } catch (error) {
      setState({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Login failed',
      });
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-700 px-4">
      <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md">
        <h1 className="text-2xl font-bold text-gray-900 text-center mb-6">Sign in to Solar Sprint</h1>

        {state.error && (
          <p className="text-red-600 text-sm text-center mb-4">{state.error}</p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              id="email"
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              id="password"
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={state.isLoading}
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {state.isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <Link href="/signup" className="text-blue-600 hover:underline font-medium">Sign up</Link>
        </p>
      </div>
    </main>
  );
}
```

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO triple backticks
- Valid TypeScript/TSX only
