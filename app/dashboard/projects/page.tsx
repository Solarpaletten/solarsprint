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

type PageState = {
  projects: Project[];
  isLoading: boolean;
  error: string | null;
};

type CreateFormState = {
  isOpen: boolean;
  name: string;
  description: string;
  isSubmitting: boolean;
  error: string | null;
};

export default function ProjectsPage() {
  const [state, setState] = useState<PageState>({
    projects: [],
    isLoading: true,
    error: null,
  });

  const [form, setForm] = useState<CreateFormState>({
    isOpen: false,
    name: '',
    description: '',
    isSubmitting: false,
    error: null,
  });

  const fetchProjects = async () => {
    try {
      const response = await fetch('/api/projects');
      if (!response.ok) throw new Error('Failed to fetch projects');
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

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name.trim()) return;

    setForm((prev) => ({ ...prev, isSubmitting: true, error: null }));

    try {
      const response = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: form.name,
          description: form.description || undefined,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to create project');
      }

      setForm({
        isOpen: false,
        name: '',
        description: '',
        isSubmitting: false,
        error: null,
      });
      fetchProjects();
    } catch (error) {
      setForm((prev) => ({
        ...prev,
        isSubmitting: false,
        error: error instanceof Error ? error.message : 'Failed to create project',
      }));
    }
  };

  const handleDelete = async (id: string, name: string) => {
    if (!window.confirm(`Delete project "${name}"?`)) return;

    try {
      const response = await fetch(`/api/projects/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete project');
      fetchProjects();
    } catch (error) {
      alert('Failed to delete project');
    }
  };

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
        <button
          onClick={() => setForm((prev) => ({ ...prev, isOpen: true }))}
          className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Project
        </button>
      </div>

      {/* Create Form */}
      {form.isOpen && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Project</h2>
          
          {form.error && (
            <p className="text-red-600 text-sm mb-4">{form.error}</p>
          )}

          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                Project Name *
              </label>
              <input
                id="name"
                type="text"
                required
                value={form.name}
                onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="My Project"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="description"
                rows={3}
                value={form.description}
                onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Project description (optional)"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={form.isSubmitting}
                className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {form.isSubmitting ? 'Creating...' : 'Create Project'}
              </button>
              <button
                type="button"
                onClick={() => setForm((prev) => ({ ...prev, isOpen: false, name: '', description: '', error: null }))}
                className="px-4 py-2 text-gray-600 font-medium rounded-lg hover:bg-gray-100 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Projects List */}
      {state.isLoading ? (
        <div className="text-gray-500">Loading projects...</div>
      ) : state.error ? (
        <div className="text-red-600">{state.error}</div>
      ) : state.projects.length === 0 ? (
        <div className="bg-white p-8 rounded-xl border border-gray-200 text-center">
          <p className="text-gray-500 mb-4">No projects yet</p>
          <button
            onClick={() => setForm((prev) => ({ ...prev, isOpen: true }))}
            className="text-blue-600 hover:underline font-medium"
          >
            Create your first project
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {state.projects.map((project) => (
            <div
              key={project.id}
              className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-2">
                <Link
                  href={`/dashboard/projects/${project.id}`}
                  className="text-lg font-semibold text-gray-900 hover:text-blue-600"
                >
                  {project.name}
                </Link>
                <button
                  onClick={() => handleDelete(project.id, project.name)}
                  className="text-red-600 hover:text-red-800 text-sm"
                  title="Delete project"
                >
                  🗑️
                </button>
              </div>
              
              {project.description && (
                <p className="text-sm text-gray-500 line-clamp-2 mb-3">
                  {project.description}
                </p>
              )}

              <div className="text-xs text-gray-400">
                Created {new Date(project.createdAt).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

