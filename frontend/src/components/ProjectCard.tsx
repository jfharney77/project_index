import { Code2, GitBranch, Clock, FileCode, Trash2, RefreshCw, Link } from 'lucide-react';
import { Project } from '../types';

interface Props {
  project: Project;
  onSelect: (project: Project) => void;
  onDelete: (id: string) => void;
  onRefresh: (id: string) => void;
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return 'Unknown';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

export function ProjectCard({ project, onSelect, onDelete, onRefresh }: Props) {
  return (
    <div
      className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-lg hover:border-blue-200 transition-all cursor-pointer group"
      onClick={() => onSelect(project)}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">{project.name}</h3>
          <p className="text-sm text-gray-500 truncate">{project.path}</p>
          {project.metadata.remote_origin && (
            <p className="text-xs text-gray-400 truncate inline-flex items-center gap-1 mt-0.5">
              <Link size={10} />
              {project.metadata.remote_origin}
            </p>
          )}
        </div>
        <div className="flex gap-1 ml-2">
          <button
            onClick={(e) => { e.stopPropagation(); onRefresh(project.id); }}
            className="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Refresh"
          >
            <RefreshCw size={14} />
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onDelete(project.id); }}
            className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Delete"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <p className="text-sm text-gray-600 line-clamp-2 mb-4">
        {project.summary || 'No summary available'}
      </p>

      <div className="flex flex-wrap gap-1.5 mb-3">
        {project.metadata.languages.slice(0, 4).map((lang) => (
          <span
            key={lang.language}
            className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700"
          >
            {lang.language}
          </span>
        ))}
      </div>

      <div className="flex items-center gap-4 text-xs text-gray-500">
        <span className="inline-flex items-center gap-1">
          <FileCode size={12} />
          {project.metadata.total_lines.toLocaleString()} lines
        </span>
        <span className="inline-flex items-center gap-1">
          <Code2 size={12} />
          {project.metadata.total_files} files
        </span>
        <span className="inline-flex items-center gap-1">
          <GitBranch size={12} />
          {project.metadata.default_branch}
          {project.metadata.branches && (
            <span className="text-gray-400">({project.metadata.branches.length})</span>
          )}
        </span>
        <span className="inline-flex items-center gap-1">
          <Clock size={12} />
          {formatDate(project.metadata.last_commit_date)}
        </span>
      </div>
    </div>
  );
}
