import { ArrowLeft, RefreshCw, GitBranch, Users, GitCommitHorizontal, Link } from 'lucide-react';
import { Project } from '../types';

interface Props {
  project: Project;
  onBack: () => void;
  onRefresh: (id: string) => void;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function ProjectDetail({ project, onBack, onRefresh }: Props) {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <button
          onClick={onBack}
          className="p-2 text-gray-500 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft size={20} />
        </button>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
          <p className="text-sm text-gray-500">{project.path}</p>
        </div>
        <button
          onClick={() => onRefresh(project.id)}
          className="inline-flex items-center gap-2 px-3 py-2 text-sm text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="text-sm text-gray-500 mb-1">Total Lines</div>
          <div className="text-2xl font-bold text-gray-900">
            {project.metadata.total_lines.toLocaleString()}
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="text-sm text-gray-500 mb-1">Files</div>
          <div className="text-2xl font-bold text-gray-900">
            {project.metadata.total_files.toLocaleString()}
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="text-sm text-gray-500 mb-1">Size</div>
          <div className="text-2xl font-bold text-gray-900">
            {formatBytes(project.metadata.total_size_bytes)}
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="text-sm text-gray-500 mb-1">Commits</div>
          <div className="text-2xl font-bold text-gray-900">
            {project.metadata.num_commits.toLocaleString()}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <GitBranch size={16} className="text-gray-400" />
          <span>Branch: <strong>{project.metadata.default_branch}</strong></span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Users size={16} className="text-gray-400" />
          <span>Contributors: <strong>{project.metadata.num_contributors}</strong></span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <GitCommitHorizontal size={16} className="text-gray-400" />
          <span>Last commit: <strong>{project.metadata.last_commit_date ? new Date(project.metadata.last_commit_date).toLocaleDateString() : 'Unknown'}</strong></span>
        </div>
        {project.metadata.remote_origin && (
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Link size={16} className="text-gray-400" />
            <span>Remote: <strong className="font-mono">{project.metadata.remote_origin}</strong></span>
          </div>
        )}
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Summary</h2>
        <p className="text-gray-700 whitespace-pre-wrap">{project.summary || 'No summary available.'}</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">How to Run</h2>
        <pre className="text-sm text-gray-700 whitespace-pre-wrap bg-gray-50 rounded-lg p-4 overflow-x-auto">
          {project.how_to_run || 'No run instructions available.'}
        </pre>
      </div>

      {project.metadata.improvements && project.metadata.improvements.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Suggested Improvements</h2>
          <ol className="space-y-4">
            {project.metadata.improvements.map((item, i) => (
              <li key={i} className="flex gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center mt-0.5">
                  {i + 1}
                </span>
                <p className="text-sm text-gray-700 leading-relaxed">{item}</p>
              </li>
            ))}
          </ol>
        </div>
      )}

      {project.metadata.branches && project.metadata.branches.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            Branches
            <span className="ml-2 text-sm font-normal text-gray-400">({project.metadata.branches.length})</span>
          </h2>
          <div className="flex flex-wrap gap-2">
            {project.metadata.branches.map((branch) => (
              <span
                key={branch}
                className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium ${
                  branch === project.metadata.default_branch
                    ? 'bg-blue-100 text-blue-700'
                    : branch.startsWith('remotes/')
                    ? 'bg-gray-100 text-gray-500'
                    : 'bg-green-50 text-green-700'
                }`}
              >
                <GitBranch size={10} />
                {branch}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Languages</h2>
        <div className="space-y-3">
          {project.metadata.languages.map((lang) => (
            <div key={lang.language}>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="font-medium text-gray-700">{lang.language}</span>
                <span className="text-gray-500">
                  {lang.lines.toLocaleString()} lines ({lang.percentage}%)
                </span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all"
                  style={{ width: `${Math.min(lang.percentage, 100)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
