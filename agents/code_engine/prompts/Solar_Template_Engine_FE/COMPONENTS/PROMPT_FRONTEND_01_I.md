// PROMPT_FRONTEND_01_I.md
// PURPOSE: Implement reusable Button component with variants
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
│   ├── Button.tsx      ← THIS FILE
│   ├── Input.tsx
│   └── Card.tsx
└── forms/
    └── AuthForm.tsx

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Keep components minimal and reusable
- Do NOT add complex animations
- Do NOT add icon library dependencies
- Use only Tailwind CSS

TARGET FILE:
components/ui/Button.tsx

TASK:
Implement reusable Button component with multiple variants, sizes, and states.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';
type ButtonSize = 'sm' | 'md' | 'lg';

type ButtonProps = {
  children: React.ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  className?: string;
};
```
IMPORTANT: These types MUST be defined and exported from the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Client Component ('use client' directive)
   - Functional component with props
   - Forward all standard button attributes

2. Variants:
   - primary: bg-blue-600, text-white, hover:bg-blue-700
   - secondary: bg-gray-100, text-gray-700, hover:bg-gray-200
   - danger: bg-red-600, text-white, hover:bg-red-700
   - ghost: bg-transparent, text-gray-600, hover:bg-gray-100

3. Sizes:
   - sm: px-3, py-1.5, text-sm
   - md: px-4, py-2, text-base (default)
   - lg: px-6, py-3, text-lg

4. States:
   - disabled: opacity-50, cursor-not-allowed
   - loading: show "Loading..." text, disabled

5. Base styles (all variants):
   - font-medium, rounded-lg, transition-colors
   - focus:outline-none, focus:ring-2, focus:ring-offset-2
   - inline-flex, items-center, justify-center

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
'use client';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';
export type ButtonSize = 'sm' | 'md' | 'lg';

export type ButtonProps = {
  children: React.ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  className?: string;
};

const variantStyles: Record<ButtonVariant, string> = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
  secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-500',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  ghost: 'bg-transparent text-gray-600 hover:bg-gray-100 focus:ring-gray-500',
};

const sizeStyles: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  type = 'button',
  onClick,
  className = '',
}: ButtonProps) {
  const isDisabled = disabled || loading;

  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  const disabledStyles = isDisabled ? 'opacity-50 cursor-not-allowed' : '';

  return (
    <button
      type={type}
      disabled={isDisabled}
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${disabledStyles} ${className}`}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
}

export default Button;
```

TECHNICAL CONSTRAINTS:
- MUST have 'use client' directive
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Export types for external use
- Export component as named export AND default export
- Use Record type for style mappings
- Handle className prop for custom styles

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript/TSX
- MUST include 'use client' directive
- MUST export types

OUTPUT FORMAT:
<complete components/ui/Button.tsx source code only>
