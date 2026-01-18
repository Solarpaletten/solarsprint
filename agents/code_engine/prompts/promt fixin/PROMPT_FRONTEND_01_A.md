// PROMPT_FRONTEND_01_A.md
// PURPOSE: Implement Root Layout with metadata and base structure
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
├── layout.tsx          ← THIS FILE
├── page.tsx
├── globals.css
├── (auth)/
│   ├── login/page.tsx
│   └── signup/page.tsx
└── (dashboard)/
    ├── layout.tsx
    ├── page.tsx
    └── projects/

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Project name: Solar Sprint
- Do NOT add authentication providers yet
- Do NOT add complex state management
- Keep it minimal for MVP v0.1

TARGET FILE:
app/layout.tsx

REQUIRED IMPORTS:
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

TASK:
Implement Root Layout — the top-level layout that wraps all pages.

REQUIRED TYPE DEFINITION (MUST BE INCLUDED IN OUTPUT):
```typescript
type RootLayoutProps = {
  children: React.ReactNode;
};
```
IMPORTANT: This type MUST be defined in the file!

FUNCTIONAL REQUIREMENTS:

1. Font setup:
   - Use Inter font from next/font/google
   - Variable: --font-inter
   - Subsets: ['latin']

2. Metadata:
   ```typescript
   export const metadata: Metadata = {
     title: 'Solar Sprint',
     description: 'Task management system for teams',
   };
   ```

3. HTML structure:
   - <html lang="en">
   - <body> with font class applied
   - {children} rendered inside body

4. Styling:
   - Apply font variable to body
   - Use Tailwind classes: antialiased
   - Background: bg-gray-50
   - Min height: min-h-screen

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'Solar Sprint',
  description: 'Task management system for teams',
};

type RootLayoutProps = {
  children: React.ReactNode;
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased bg-gray-50 min-h-screen`}>
        {children}
      </body>
    </html>
  );
}
```

TECHNICAL CONSTRAINTS:
- Use Next.js 14 App Router conventions
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Do NOT use styled-components or CSS modules
- Do NOT add providers or context yet
- Export metadata as const
- Export RootLayout as default function

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript/TSX
- MUST include type RootLayoutProps definition
- MUST include metadata export

OUTPUT FORMAT:
<complete app/layout.tsx source code only>
