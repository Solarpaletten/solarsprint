// PROMPT_FRONTEND_01_K.md
// PURPOSE: Implement reusable Card component with header and footer slots
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
│   ├── Input.tsx
│   └── Card.tsx        ← THIS FILE
└── forms/
    └── AuthForm.tsx

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Keep components minimal and reusable
- Do NOT add collapse/expand functionality
- Do NOT add drag-and-drop
- Use only Tailwind CSS

TARGET FILE:
components/ui/Card.tsx

TASK:
Implement reusable Card component with optional header, footer, and padding variants.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type CardProps = {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  footer?: React.ReactNode;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  className?: string;
};
```
IMPORTANT: This type MUST be defined and exported from the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Server Component (NO 'use client' needed)
   - Functional component with props
   - Composable with slots (header, content, footer)

2. Structure:
   - Optional header: title + subtitle
   - Content area: children
   - Optional footer: custom content

3. Variants:
   - padding: none (p-0), sm (p-4), md (p-6), lg (p-8)
   - hover: adds hover:shadow-md effect

4. Styling (Tailwind classes):
   - Container: bg-white, rounded-xl, shadow-sm, border, border-gray-100
   - Header: border-b, border-gray-100 (only if title exists)
   - Title: text-lg, font-semibold, text-gray-900
   - Subtitle: text-sm, text-gray-500, mt-1
   - Footer: border-t, border-gray-100, bg-gray-50

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
export type CardProps = {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  footer?: React.ReactNode;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  className?: string;
};

const paddingStyles = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
};

export function Card({
  children,
  title,
  subtitle,
  footer,
  padding = 'md',
  hover = false,
  className = '',
}: CardProps) {
  const baseStyles = 'bg-white rounded-xl shadow-sm border border-gray-100';
  const hoverStyles = hover ? 'hover:shadow-md transition-shadow' : '';

  return (
    <div className={`${baseStyles} ${hoverStyles} ${className}`}>
      {/* Header */}
      {title && (
        <div className={`${paddingStyles[padding]} border-b border-gray-100`}>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
      )}

      {/* Content */}
      <div className={paddingStyles[padding]}>
        {children}
      </div>

      {/* Footer */}
      {footer && (
        <div className={`${paddingStyles[padding]} border-t border-gray-100 bg-gray-50 rounded-b-xl`}>
          {footer}
        </div>
      )}
    </div>
  );
}

export default Card;
```

TECHNICAL CONSTRAINTS:
- Do NOT use 'use client' (Server Component)
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Export type for external use
- Export component as named export AND default export
- Handle optional header/footer gracefully

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript/TSX
- NO 'use client' directive (Server Component)
- MUST export types

OUTPUT FORMAT:
<complete components/ui/Card.tsx source code only>
