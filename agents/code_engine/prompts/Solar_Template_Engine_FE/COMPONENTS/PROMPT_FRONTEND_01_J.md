// PROMPT_FRONTEND_01_J.md
// PURPOSE: Implement reusable Input component with password visibility toggle
// VERSION: 2.0 — Added eye icon for password fields

ROLE: SENIOR FRONTEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack: Next.js 14, TypeScript, React 18, Tailwind CSS

TARGET FILE: components/ui/Input.tsx

TASK:
Create a reusable Input component with label, error handling, and password visibility toggle.

REQUIRED TYPE DEFINITIONS:
```typescript
export type InputProps = {
  id: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  autoComplete?: string;
  className?: string;
};
```

FUNCTIONAL REQUIREMENTS:
1. 'use client' directive (uses useState for password visibility)
2. Import useState from react
3. Label with optional required asterisk (*)
4. Input field with Tailwind styling
5. Error message display (red text below input)
6. Disabled state styling
7. **PASSWORD VISIBILITY TOGGLE:**
   - Show eye icon button ONLY for type="password"
   - Click toggles between password/text
   - Icon: 👁️ (show) / 👁️‍🗨️ (hide) — use emoji for simplicity
   - Button positioned inside input on the right

STYLING:
- Container: w-full
- Label: block text-sm font-medium text-gray-700 mb-1
- Input wrapper: relative (for eye icon positioning)
- Input: w-full px-4 py-3 border rounded-lg transition-colors focus:outline-none
- Normal border: border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent
- Error border: border-red-500 focus:ring-2 focus:ring-red-500
- Disabled: opacity-50 cursor-not-allowed bg-gray-50
- Eye button: absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700
- When password field: add pr-12 to input for eye icon space

COMPLETE CODE STRUCTURE:
```typescript
'use client';

import { useState } from 'react';

export type InputProps = {
  id: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url';
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  autoComplete?: string;
  className?: string;
};

export function Input({
  id,
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  required = false,
  disabled = false,
  autoComplete,
  className = '',
}: InputProps) {
  const [showPassword, setShowPassword] = useState(false);
  
  const isPassword = type === 'password';
  const inputType = isPassword && showPassword ? 'text' : type;

  const baseInputStyles = 'w-full px-4 py-3 border rounded-lg transition-colors focus:outline-none';
  const normalStyles = 'border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent';
  const errorStyles = 'border-red-500 focus:ring-2 focus:ring-red-500';
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed bg-gray-50' : '';
  const passwordPadding = isPassword ? 'pr-12' : '';

  return (
    <div className={`w-full ${className}`}>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>

      <div className="relative">
        <input
          id={id}
          name={id}
          type={inputType}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          required={required}
          disabled={disabled}
          autoComplete={autoComplete}
          className={`${baseInputStyles} ${error ? errorStyles : normalStyles} ${disabledStyles} ${passwordPadding}`}
        />

        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
            tabIndex={-1}
          >
            {showPassword ? '👁️‍🗨️' : '👁️'}
          </button>
        )}
      </div>

      {error && (
        <p className="text-red-600 text-sm mt-1">{error}</p>
      )}
    </div>
  );
}

export default Input;
```

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO triple backticks
- Valid TypeScript/TSX only
