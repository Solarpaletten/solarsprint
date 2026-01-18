// PROMPT_FRONTEND_01_L.md
// PURPOSE: Implement reusable AuthForm component for login and signup
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
components/
├── ui/
│   ├── Button.tsx      ← USES THIS
│   ├── Input.tsx       ← USES THIS
│   └── Card.tsx
└── forms/
    └── AuthForm.tsx    ← THIS FILE

EXISTING COMPONENTS (ALREADY IMPLEMENTED):
- Button: import { Button } from '@/components/ui/Button'
- Input: import { Input } from '@/components/ui/Input'

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Keep components minimal and reusable
- Use existing Button and Input components
- Do NOT add OAuth buttons
- Do NOT add password strength indicator

TARGET FILE:
components/forms/AuthForm.tsx

TASK:
Implement reusable AuthForm component that can be used for both login and signup forms.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type AuthFormMode = 'login' | 'signup';

type AuthFormProps = {
  mode: AuthFormMode;
  onSubmit: (data: AuthFormData) => Promise<void>;
  error?: string | null;
  isLoading?: boolean;
};

type AuthFormData = {
  name?: string;
  email: string;
  password: string;
};
```
IMPORTANT: These types MUST be defined and exported from the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Client Component ('use client' directive)
   - Uses existing Button and Input components
   - Handles form state internally

2. Modes:
   - login: email + password fields
   - signup: name + email + password + confirmPassword fields

3. Form fields:
   - Name (signup only): text, required
   - Email: email, required
   - Password: password, required, minLength 8
   - Confirm Password (signup only): password, required, must match

4. Validation:
   - All required fields must be filled
   - Passwords must match (signup mode)
   - Password min 8 characters

5. Props:
   - mode: 'login' | 'signup'
   - onSubmit: async function receiving form data
   - error: external error message to display
   - isLoading: shows loading state on button

6. UI Structure:
   - Title: "Sign In" or "Create Account"
   - Error message (if any)
   - Form fields
   - Submit button
   - Link to opposite mode

7. Styling:
   - Card-like container with padding
   - Space between fields (space-y-4)
   - Centered title

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

export type AuthFormMode = 'login' | 'signup';

export type AuthFormData = {
  name?: string;
  email: string;
  password: string;
};

export type AuthFormProps = {
  mode: AuthFormMode;
  onSubmit: (data: AuthFormData) => Promise<void>;
  error?: string | null;
  isLoading?: boolean;
};

type FormState = {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
};

type FormErrors = {
  name?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
};

export function AuthForm({ mode, onSubmit, error, isLoading = false }: AuthFormProps) {
  const [form, setForm] = useState<FormState>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});

  const isLogin = mode === 'login';
  const title = isLogin ? 'Sign In' : 'Create Account';
  const submitText = isLogin ? 'Sign In' : 'Create Account';
  const loadingText = isLogin ? 'Signing in...' : 'Creating account...';
  const switchText = isLogin
    ? "Don't have an account?"
    : 'Already have an account?';
  const switchLink = isLogin ? '/signup' : '/login';
  const switchLinkText = isLogin ? 'Sign up' : 'Sign in';

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!isLogin && !form.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!form.email.trim()) {
      newErrors.email = 'Email is required';
    }

    if (!form.password) {
      newErrors.password = 'Password is required';
    } else if (form.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!isLogin && form.password !== form.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) return;

    await onSubmit({
      ...(isLogin ? {} : { name: form.name }),
      email: form.email,
      password: form.password,
    });
  };

  const handleChange = (field: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
    setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  return (
    <div className="w-full max-w-md">
      <h1 className="text-2xl font-bold text-gray-900 text-center mb-6">
        {title}
      </h1>

      {error && (
        <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg mb-4 text-center">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {!isLogin && (
          <Input
            id="name"
            label="Name"
            type="text"
            placeholder="John Doe"
            value={form.name}
            onChange={handleChange('name')}
            error={errors.name}
            required
          />
        )}

        <Input
          id="email"
          label="Email"
          type="email"
          placeholder="you@example.com"
          value={form.email}
          onChange={handleChange('email')}
          error={errors.email}
          required
          autoComplete="email"
        />

        <Input
          id="password"
          label="Password"
          type="password"
          placeholder="••••••••"
          value={form.password}
          onChange={handleChange('password')}
          error={errors.password}
          required
          autoComplete={isLogin ? 'current-password' : 'new-password'}
        />

        {!isLogin && (
          <Input
            id="confirmPassword"
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
            value={form.confirmPassword}
            onChange={handleChange('confirmPassword')}
            error={errors.confirmPassword}
            required
            autoComplete="new-password"
          />
        )}

        <Button
          type="submit"
          variant="primary"
          size="lg"
          loading={isLoading}
          disabled={isLoading}
          className="w-full"
        >
          {isLoading ? loadingText : submitText}
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-gray-600">
        {switchText}{' '}
        <Link href={switchLink} className="text-blue-600 hover:underline font-medium">
          {switchLinkText}
        </Link>
      </p>
    </div>
  );
}

export default AuthForm;
```

TECHNICAL CONSTRAINTS:
- MUST have 'use client' directive (client component)
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- MUST use existing Button and Input components
- Export types for external use
- Export component as named export AND default export
- Handle validation internally
- Clear field error on change

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript/TSX
- MUST include 'use client' directive
- MUST export types
- MUST import from @/components/ui/

OUTPUT FORMAT:
<complete components/forms/AuthForm.tsx source code only>
