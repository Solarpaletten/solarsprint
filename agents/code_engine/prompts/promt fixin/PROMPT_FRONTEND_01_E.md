// PROMPT_FRONTEND_01_E.md
// PURPOSE: Implement Dashboard Layout with sidebar navigation
// VERSION: 2.0 — Fixed: correct paths for dashboard folder structure

ROLE: SENIOR FRONTEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack: Next.js 14 (App Router), TypeScript, React 18, Tailwind CSS

TARGET FILE: app/dashboard/layout.tsx

NOTE: This file is in app/dashboard/ (NOT app/(dashboard)/)

TASK:
Create Dashboard Layout with sidebar navigation.

NAVIGATION PATHS (IMPORTANT):
- Dashboard: /dashboard
- Projects: /dashboard/projects
- Logout: clears localStorage, redirects to /login

REQUIRED TYPE DEFINITIONS:
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

FUNCTIONAL REQUIREMENTS:
1. 'use client' directive
2. Import usePathname, useRouter from 'next/navigation'
3. Import Link from 'next/link'
4. Fixed sidebar (w-64) + Main content (flex-1)
5. Logo: "Solar Sprint" linking to /dashboard
6. Navigation items with active state highlighting
7. Logout button that clears localStorage and redirects

NAV ITEMS:
```typescript
const navItems: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: '📊' },
  { name: 'Projects', href: '/dashboard/projects', icon: '📁' },
];
```

COMPLETE CODE STRUCTURE:
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
    localStorage.removeItem('userId');
    localStorage.removeItem('tenantId');
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

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO triple backticks
- Valid TypeScript/TSX only
