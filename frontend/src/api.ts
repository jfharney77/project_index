import { Project } from './types';

const API_BASE = '/projects';

export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(API_BASE);
  if (!res.ok) throw new Error('Failed to fetch projects');
  return res.json();
}

export async function fetchProject(id: string): Promise<Project> {
  const res = await fetch(`${API_BASE}/${id}`);
  if (!res.ok) throw new Error('Failed to fetch project');
  return res.json();
}

export async function addProject(path: string): Promise<Project> {
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path }),
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.detail || 'Failed to add project');
  }
  return res.json();
}

export async function deleteProject(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete project');
}

export async function refreshProject(id: string): Promise<Project> {
  const res = await fetch(`${API_BASE}/${id}/refresh`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to refresh project');
  return res.json();
}
