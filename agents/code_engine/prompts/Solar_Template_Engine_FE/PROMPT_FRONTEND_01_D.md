// PROMPT_FRONTEND_01_D.md
// PURPOSE: Implement Signup Page with form and API integration
// VERSION: 1.0

ROLE: SENIOR FRONTEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- TypeScript (strict mode)
- React 18
- Tailwind CSS (utility classes only)

PROJECT STRUCTURE:
app/
├── layout.tsx
├── page.tsx
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── signup/
│       └── page.tsx    ← THIS FILE
└── (dashboard)/

API ENDPOINT (ALREADY IMPLEMENTED):
POST /api/auth/signup
Request: { email: string, password: string, name: string }
Response Success: { user: { id, email, tenantId }, token: string }
Response Error: { error: string }

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Project name: Solar Sprint
- Keep it minimal for MVP v0.1
- Do NOT add OAuth providers
- Do NOT add terms checkbox yet
- Do NOT add email verification yet

TARGET FILE:
app/(auth)/signup/page.tsx

REQUIRED IMPORTS:
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

TASK:
Implement Signup Page — client component with form, validation, and API call.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type SignupFormData = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
};

type SignupState = {
  isLoading: boolean;
  error: string | null;
};
```
IMPORTANT: These types MUST be defined in the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Client Component ('use client' directive)
   - Uses useState for form data and loading state
   - Uses useRouter for navigation after signup

2. Form fields:
   - Name: type="text", required
   - Email: type="email", required
   - Password: type="password", required, minLength=8
   - Confirm Password: type="password", required
   - Submit button: "Create Account"

3. Form validation:
   - All fields required
   - Password minimum 8 characters
   - Passwords must match (client-side check)

4. Form handling:
   - Controlled inputs with useState
   - onSubmit handler with preventDefault
   - Validate passwords match before API call
   - Call POST /api/auth/signup (send name, email, password — NOT confirmPassword)
   - On success: router.push('/dashboard')
   - On error: display error message

5. UI states:
   - Default: form ready
   - Loading: button disabled, show "Creating account..."
   - Error: show error message above form

6. Layout:
   - Centered card on gradient background
   - Card: white background, rounded, shadow
   - Link to login: "Already have an account? Sign in"

7. Styling (Tailwind classes):
   - Page: min-h-screen, flex, items-center, justify-center, bg-gradient-to-br from-blue-600 to-indigo-700
   - Card: bg-white, p-8, rounded-xl, shadow-xl, w-full, max-w-md
   - Title: text-2xl, font-bold, text-gray-900, text-center, mb-6
   - Input: w-full, px-4, py-3, border, border-gray-300, rounded-lg, focus:ring-2, focus:ring-blue-500, focus:border-transparent
   - Label: block, text-sm, font-medium, text-gray-700, mb-1
   - Button: w-full, py-3, bg-blue-600, text-white, font-semibold, rounded-lg, hover:bg-blue-700, disabled:opacity-50
   - Error: text-red-600, text-sm, text-center, mb-4
   - Link: text-blue-600, hover:underline

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

type SignupFormData = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
};

type SignupState = {
  isLoading: boolean;
  error: string | null;
};

export default function SignupPage() {
  const router = useRouter();
  
  const [formData, setFormData] = useState<SignupFormData>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  
  const [state, setState] = useState<SignupState>({
    isLoading: false,
    error: null,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setState({ isLoading: false, error: 'Passwords do not match' });
      return;
    }

    // Validate password length
    if (formData.password.length < 8) {
      setState({ isLoading: false, error: 'Password must be at least 8 characters' });
      return;
    }

    setState({ isLoading: true, error: null });

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Signup failed');
      }

      router.push('/dashboard');
    } catch (error) {
      setState({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Signup failed',
      });
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-700 px-4">
      <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md">
        {/* Title */}
        <h1 className="text-2xl font-bold text-gray-900 text-center mb-6">
          Create your account
        </h1>

        {/* Error message */}
        {state.error && (
          <p className="text-red-600 text-sm text-center mb-4">
            {state.error}
          </p>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Name */}
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Name
            </label>
            <input
              id="name"
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="John Doe"
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
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

          {/* Password */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              minLength={8}
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="••••••••"
            />
          </div>

          {/* Confirm Password */}
          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              required
              value={formData.confirmPassword}
              onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="••••••••"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={state.isLoading}
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {state.isLoading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        {/* Sign in link */}
        <p className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/login" className="text-blue-600 hover:underline font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
```

TECHNICAL CONSTRAINTS:
- Use Next.js 14 App Router conventions
- MUST have 'use client' directive (client component)
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Use next/navigation for router (NOT next/router)
- Use next/link for navigation links
- Handle loading and error states
- Use controlled form inputs
- Validate passwords match BEFORE API call
- Do NOT send confirmPassword to API

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript/TSX
- MUST include 'use client' directive
- MUST include type definitions

OUTPUT FORMAT:
<complete app/(auth)/signup/page.tsx source code only>
