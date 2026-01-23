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
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          New Project
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

