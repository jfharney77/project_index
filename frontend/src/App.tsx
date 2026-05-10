import { useState, useEffect } from 'react';
import { Database } from 'lucide-react';
import { Project } from './types';
import { fetchProjects, addProject, deleteProject, refreshProject } from './api';
import { AddProjectDialog } from './components/AddProjectDialog';
import { ProjectCard } from './components/ProjectCard';
import { ProjectDetail } from './components/ProjectDetail';

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadProjects = async () => {
    try {
      const data = await fetchProjects();
      setProjects(data);
      setError('');
    } catch {
      setError('Failed to load projects. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleAdd = async (path: string) => {
    const project = await addProject(path);
    setProjects((prev) => [...prev, project]);
  };

  const handleDelete = async (id: string) => {
    await deleteProject(id);
    setProjects((prev) => prev.filter((p) => p.id !== id));
    if (selectedProject?.id === id) {
      setSelectedProject(null);
    }
  };

  const handleRefresh = async (id: string) => {
    const updated = await refreshProject(id);
    setProjects((prev) => prev.map((p) => (p.id === id ? updated : p)));
    if (selectedProject?.id === id) {
      setSelectedProject(updated);
    }
  };

  if (selectedProject) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ProjectDetail
          project={selectedProject}
          onBack={() => setSelectedProject(null)}
          onRefresh={handleRefresh}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database className="text-blue-600" size={28} />
            <h1 className="text-xl font-bold text-gray-900">Project Index</h1>
          </div>
          <AddProjectDialog onAdd={handleAdd} />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {loading && (
          <div className="text-center py-12 text-gray-500">Loading projects...</div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 mb-6">
            {error}
          </div>
        )}

        {!loading && !error && projects.length === 0 && (
          <div className="text-center py-16">
            <Database className="mx-auto text-gray-300 mb-4" size={48} />
            <h2 className="text-lg font-medium text-gray-600 mb-2">No projects indexed yet</h2>
            <p className="text-gray-500">
              Click "Add Project" to index your first local git repository.
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onSelect={setSelectedProject}
              onDelete={handleDelete}
              onRefresh={handleRefresh}
            />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
