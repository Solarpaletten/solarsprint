// PROMPT_FRONTEND_01_J.md
// PURPOSE: Implement reusable Input component with label and error state
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
│   ├── Button.tsx
│   ├── Input.tsx       ← THIS FILE
│   └── Card.tsx
└── forms/
    └── AuthForm.tsx

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Keep components minimal and reusable
- Do NOT add input masking
- Do NOT add complex validation
- Use only Tailwind CSS

TARGET FILE:
components/ui/Input.tsx

TASK:
Implement reusable Input component with label, error message, and various input types.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type InputProps = {
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
IMPORTANT: This type MUST be defined and exported from the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Client Component ('use client' directive)
   - Functional component with props
   - Controlled input (value + onChange)

2. Structure:
   - Label above input
   - Input field
   - Error message below (conditional)

3. States:
   - Default: gray border
   - Focus: blue ring
   - Error: red border, red error text
   - Disabled: opacity-50, cursor-not-allowed

4. Styling (Tailwind classes):
   - Wrapper: w-full
   - Label: block, text-sm, font-medium, text-gray-700, mb-1
   - Input: w-full, px-4, py-3, border, rounded-lg, transition-colors
   - Input default: border-gray-300, focus:ring-2, focus:ring-blue-500, focus:border-transparent
   - Input error: border-red-500, focus:ring-red-500
   - Error text: text-red-600, text-sm, mt-1

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
'use client';

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
  const baseInputStyles = 'w-full px-4 py-3 border rounded-lg transition-colors focus:outline-none focus:ring-2 focus:border-transparent';
  const normalStyles = 'border-gray-300 focus:ring-blue-500';
  const errorStyles = 'border-red-500 focus:ring-red-500';
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed bg-gray-50' : '';

  return (
    <div className={`w-full ${className}`}>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <input
        id={id}
        name={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        autoComplete={autoComplete}
        className={`${baseInputStyles} ${error ? errorStyles : normalStyles} ${disabledStyles}`}
      />
      
      {error && (
        <p className="text-red-600 text-sm mt-1">{error}</p>
      )}
    </div>
  );
}

export default Input;
```

TECHNICAL CONSTRAINTS:
- MUST have 'use client' directive
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Export type for external use
- Export component as named export AND default export
- Use controlled input pattern
- Show required indicator (*) when required=true

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
<complete components/ui/Input.tsx source code only>
