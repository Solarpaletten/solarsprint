// PROMPT_FRONTEND_01_E.md
// PURPOSE: Implement Dashboard Layout with sidebar navigation
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
│   ├── login/page.tsx
│   └── signup/page.tsx
└── (dashboard)/
    ├── layout.tsx      ← THIS FILE
    ├── page.tsx
    └── projects/
        ├── page.tsx
        └── [id]/page.tsx

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Project name: Solar Sprint
- Keep it minimal for MVP v0.1
- Do NOT add complex navigation state
- Do NOT add user avatar/profile yet
- Do NOT add notifications

TARGET FILE:
app/(dashboard)/layout.tsx

REQUIRED IMPORTS:
'use client';

import { usePathname, useRouter } from 'next/navigation';
import Link from 'next/link';

TASK:
Implement Dashboard Layout — wrapper for all authenticated pages with sidebar navigation.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type DashboardLayoutProps = {
  children: React.ReactNode;
};

type NavItem = {
  name: string;
  href: string;
  icon: string;
};
```
IMPORTANT: These types MUST be defined in the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Client Component ('use client' directive)
   - Uses usePathname to highlight active nav item
   - Uses useRouter for logout redirect

2. Layout structure:
   - Fixed sidebar on left (w-64)
   - Main content area on right (flex-1)
   - Full height layout (min-h-screen)

3. Sidebar content:
   - Logo/Brand: "Solar Sprint" at top
   - Navigation items:
     - Dashboard (icon: 📊) → /dashboard
     - Projects (icon: 📁) → /dashboard/projects
   - Logout button at bottom

4. Navigation highlighting:
   - Active item: bg-blue-100 text-blue-700
   - Inactive item: text-gray-600 hover:bg-gray-100

5. Logout functionality:
   - Clear any stored token (localStorage)
   - Redirect to /login

6. Styling (Tailwind classes):
   - Layout: flex, min-h-screen
   - Sidebar: w-64, bg-white, border-r, border-gray-200, flex, flex-col
   - Logo area: p-6, border-b, border-gray-200
   - Logo text: text-xl, font-bold, text-blue-600
   - Nav: flex-1, p-4
   - Nav item: flex, items-center, gap-3, px-4, py-3, rounded-lg, text-sm, font-medium
   - Main content: flex-1, bg-gray-50
   - Logout button: mx-4, mb-4, px-4, py-3, text-red-600, hover:bg-red-50, rounded-lg

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
'use client';

import { usePathname, useRouter } from 'next/navigation';
import Link from 'next/link';

type DashboardLayoutProps = {
  children: React.ReactNode;
};

type NavItem = {
  name: string;
  href: string;
  icon: string;
};

const navItems: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: '📊' },
  { name: 'Projects', href: '/dashboard/projects', icon: '📁' },
];

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return pathname === '/dashboard';
    }
    return pathname.startsWith(href);
  };

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-gray-200">
          <Link href="/dashboard" className="text-xl font-bold text-blue-600">
            Solar Sprint
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {navItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                    isActive(item.href)
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-gray-200">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <span>🚪</span>
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 bg-gray-50">
        {children}
      </main>
    </div>
  );
}
```

TECHNICAL CONSTRAINTS:
- Use Next.js 14 App Router conventions
- MUST have 'use client' directive (client component)
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Use next/navigation for usePathname and useRouter
- Use next/link for navigation links
- Use emoji icons (📊, 📁, 🚪) for simplicity
- Export DashboardLayout as default function

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
<complete app/(dashboard)/layout.tsx source code only>
