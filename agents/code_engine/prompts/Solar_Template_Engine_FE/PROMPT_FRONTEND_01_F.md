// PROMPT_FRONTEND_01_F.md
// PURPOSE: Implement Dashboard Home Page with welcome message and stats
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
    ├── layout.tsx
    ├── page.tsx        ← THIS FILE
    └── projects/
        ├── page.tsx
        └── [id]/page.tsx

API ENDPOINTS (ALREADY IMPLEMENTED):
GET /api/projects
Response: [{ id, name, description, tenantId, createdAt, updatedAt }, ...]

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Project name: Solar Sprint
- Keep it minimal for MVP v0.1
- Do NOT add complex charts yet
- Do NOT add activity feed yet
- Do NOT add team members list

TARGET FILE:
app/(dashboard)/page.tsx

REQUIRED IMPORTS:
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

TASK:
Implement Dashboard Home Page — welcome screen with project stats and quick actions.

REQUIRED TYPE DEFINITIONS (MUST BE INCLUDED IN OUTPUT):
```typescript
type Project = {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
};

type DashboardState = {
  projects: Project[];
  isLoading: boolean;
  error: string | null;
};
```
IMPORTANT: These types MUST be defined in the file!

FUNCTIONAL REQUIREMENTS:

1. Component type:
   - Client Component ('use client' directive)
   - Uses useState for data and loading state
   - Uses useEffect to fetch data on mount

2. Data fetching:
   - Fetch projects from GET /api/projects
   - Display total count in stats card
   - Show recent projects (last 3)

3. Page sections:
   a. Header: "Welcome to Solar Sprint" + subtitle
   b. Stats cards: Total Projects count
   c. Quick actions: "New Project" button
   d. Recent projects: List of last 3 projects with links

4. UI states:
   - Loading: Show skeleton/loading text
   - Error: Show error message
   - Empty: Show "No projects yet" message
   - Data: Show stats and recent projects

5. Styling (Tailwind classes):
   - Container: p-8
   - Header: mb-8
   - Title: text-3xl, font-bold, text-gray-900
   - Subtitle: text-gray-600, mt-2
   - Stats grid: grid, grid-cols-1, md:grid-cols-3, gap-6, mb-8
   - Stat card: bg-white, p-6, rounded-xl, shadow-sm, border, border-gray-100
   - Stat number: text-3xl, font-bold, text-blue-600
   - Stat label: text-sm, text-gray-500, mt-1
   - Section title: text-xl, font-semibold, text-gray-900, mb-4
   - Project card: bg-white, p-4, rounded-lg, border, border-gray-200, hover:border-blue-300
   - Button: px-4, py-2, bg-blue-600, text-white, rounded-lg, hover:bg-blue-700

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

type Project = {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
};

type DashboardState = {
  projects: Project[];
  isLoading: boolean;
  error: string | null;
};

export default function DashboardPage() {
  const [state, setState] = useState<DashboardState>({
    projects: [],
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await fetch('/api/projects');
        
        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }
        
        const projects = await response.json();
        setState({ projects, isLoading: false, error: null });
      } catch (error) {
        setState({
          projects: [],
          isLoading: false,
          error: error instanceof Error ? error.message : 'Failed to load data',
        });
      }
    };

    fetchProjects();
  }, []);

  const recentProjects = state.projects.slice(0, 3);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome to Solar Sprint
        </h1>
        <p className="text-gray-600 mt-2">
          Manage your projects and track progress
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-blue-600">
            {state.isLoading ? '...' : state.projects.length}
          </div>
          <div className="text-sm text-gray-500 mt-1">Total Projects</div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-green-600">
            {state.isLoading ? '...' : state.projects.length}
          </div>
          <div className="text-sm text-gray-500 mt-1">Active Projects</div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-purple-600">0</div>
          <div className="text-sm text-gray-500 mt-1">Completed Tasks</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <Link
          href="/dashboard/projects"
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <span>📁</span>
          <span>View All Projects</span>
        </Link>
      </div>

      {/* Recent Projects */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Recent Projects
        </h2>

        {state.isLoading ? (
          <div className="text-gray-500">Loading projects...</div>
        ) : state.error ? (
          <div className="text-red-600">{state.error}</div>
        ) : recentProjects.length === 0 ? (
          <div className="bg-white p-6 rounded-lg border border-gray-200 text-center">
            <p className="text-gray-500 mb-4">No projects yet</p>
            <Link
              href="/dashboard/projects"
              className="text-blue-600 hover:underline font-medium"
            >
              Create your first project
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {recentProjects.map((project) => (
              <Link
                key={project.id}
                href={`/dashboard/projects/${project.id}`}
                className="block bg-white p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors"
              >
                <h3 className="font-medium text-gray-900">{project.name}</h3>
                {project.description && (
                  <p className="text-sm text-gray-500 mt-1 line-clamp-1">
                    {project.description}
                  </p>
                )}
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
```

TECHNICAL CONSTRAINTS:
- Use Next.js 14 App Router conventions
- MUST have 'use client' directive (client component)
- Use TypeScript strict mode
- Use Tailwind CSS utility classes only
- Use next/link for navigation links
- Fetch data in useEffect on component mount
- Handle loading, error, and empty states
- Export DashboardPage as default function

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
<complete app/(dashboard)/page.tsx source code only>
