// PROMPT_FRONTEND_01_F.md
// PURPOSE: Implement Dashboard Home Page with authenticated API calls
// VERSION: 2.0 — Fixed: send x-user-id header for authentication

ROLE: SENIOR FRONTEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack: Next.js 14 (App Router), TypeScript, React 18, Tailwind CSS

TARGET FILE: app/dashboard/page.tsx

NOTE: This file is in app/dashboard/ (NOT app/(dashboard)/)

TASK:
Create Dashboard Home Page with stats and recent projects.

AUTHENTICATION:
All API calls MUST include x-user-id header from localStorage!
```typescript
const userId = localStorage.getItem('userId');
headers: { 'x-user-id': userId || '' }
```

REQUIRED TYPE DEFINITIONS:
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

FUNCTIONAL REQUIREMENTS:
1. 'use client' directive
2. Import useState, useEffect from 'react'
3. Import Link from 'next/link'
4. useEffect to fetch projects on mount
5. GET /api/projects WITH x-user-id header
6. Stats cards: Total Projects, Active Projects, Completed Tasks (placeholder 0)
7. Recent projects section (last 3)
8. Loading / Error / Empty states
9. "New Project" button → link to /dashboard/projects

COMPLETE CODE STRUCTURE:
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
        const userId = localStorage.getItem('userId');
        
        const response = await fetch('/api/projects', {
          headers: {
            'x-user-id': userId || '',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch projects');
        }

        const projects = await response.json();
        setState({ projects, isLoading: false, error: null });
      } catch (error) {
        setState({
          projects: [],
          isLoading: false,
          error: error instanceof Error ? error.message : 'Failed to load projects',
        });
      }
    };

    fetchProjects();
  }, []);

  const recentProjects = state.projects.slice(0, 3);

  if (state.isLoading) {
    return (
      <div className="p-8">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to Solar Sprint</h1>
      <p className="text-gray-600 mb-8">Manage your projects and track progress</p>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-blue-600">{state.projects.length}</div>
          <div className="text-gray-500">Total Projects</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-green-600">{state.projects.length}</div>
          <div className="text-gray-500">Active Projects</div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-purple-600">0</div>
          <div className="text-gray-500">Completed Tasks</div>
        </div>
      </div>

      {/* New Project Button */}
      <Link
        href="/dashboard/projects"
        className="inline-block px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors mb-8"
      >
        New Project
      </Link>

      {/* Recent Projects */}
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Projects</h2>

      {state.error && (
        <p className="text-red-600 mb-4">{state.error}</p>
      )}

      {recentProjects.length === 0 ? (
        <p className="text-gray-500">No projects yet. Create your first project!</p>
      ) : (
        <div className="space-y-4">
          {recentProjects.map((project) => (
            <Link
              key={project.id}
              href={`/dashboard/projects/${project.id}`}
              className="block bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <h3 className="font-medium text-gray-900">{project.name}</h3>
              {project.description && (
                <p className="text-gray-500 text-sm mt-1">{project.description}</p>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
```

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO triple backticks
- Valid TypeScript/TSX only
