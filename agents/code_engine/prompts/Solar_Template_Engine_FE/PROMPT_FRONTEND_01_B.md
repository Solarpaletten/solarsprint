// PROMPT_FRONTEND_01_B.md
// PURPOSE: Implement Landing Page with hero section and CTA
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
├── page.tsx            ← THIS FILE
├── globals.css
├── (auth)/
│   ├── login/page.tsx
│   └── signup/page.tsx
└── (dashboard)/

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Project name: Solar Sprint
- Keep it minimal for MVP v0.1
- Do NOT add complex animations
- Do NOT fetch data on this page

TARGET FILE:
app/page.tsx

REQUIRED IMPORTS:
import Link from 'next/link';

TASK:
Implement Landing Page — the public homepage with hero section and call-to-action buttons.

FUNCTIONAL REQUIREMENTS:

1. Page type:
   - Server Component (default, no 'use client')
   - No state, no hooks needed

2. Layout structure:
   - Full-screen hero section
   - Centered content
   - Navigation links to /login and /signup

3. Content:
   - Logo/Title: "Solar Sprint"
   - Tagline: "Task management for modern teams"
   - Description: Brief 1-2 sentence description
   - CTA buttons: "Get Started" → /signup, "Sign In" → /login

4. Styling (Tailwind classes):
   - Container: min-h-screen, flex, items-center, justify-center
   - Background: bg-gradient-to-br from-blue-600 to-indigo-700
   - Text: text-white
   - Title: text-5xl font-bold
   - Tagline: text-xl text-blue-100
   - Buttons: rounded-lg, px-6, py-3, font-semibold
   - Primary button (Get Started): bg-white text-blue-600 hover:bg-blue-50
   - Secondary button (Sign In): border border-white text-white hover:bg-white/10

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-700">
      <div className="text-center px-4">
        {/* Logo/Title */}
        <h1 className="text-5xl font-bold text-white mb-4">
          Solar Sprint
        </h1>
        
        {/* Tagline */}
        <p className="text-xl text-blue-100 mb-2">
          Task management for modern teams
        </p>
        
        {/* Description */}
        <p className="text-blue-200 mb-8 max-w-md mx-auto">
          Organize your projects, track progress, and collaborate 
          with your team in one powerful platform.
        </p>
        
        {/* CTA Buttons */}
        <div className="flex gap-4 justify-center">
          <Link
            href="/signup"
            className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-6 py-3 border border-white text-white font-semibold rounded-lg hover:bg-white/10 transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </main>
  );
}
```

TECHNICAL CONSTRAINTS:
- Use Next.js 14 App Router conventions
- Use TypeScript
- Use Tailwind CSS utility classes only
- Use next/link for navigation (NOT <a> tags)
- Server Component (no 'use client' directive)
- Do NOT use any hooks or state
- Do NOT fetch any data
- Export HomePage as default function

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript/TSX

OUTPUT FORMAT:
<complete app/page.tsx source code only>
