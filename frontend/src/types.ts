export interface LanguageStats {
  language: string;
  files: number;
  lines: number;
  percentage: number;
}

export interface ProjectMetadata {
  total_files: number;
  total_lines: number;
  total_size_bytes: number;
  languages: LanguageStats[];
  predominant_language: string;
  last_commit_date: string | null;
  default_branch: string;
  num_commits: number;
  num_contributors: number;
}

export interface Project {
  id: string;
  name: string;
  path: string;
  summary: string;
  how_to_run: string;
  metadata: ProjectMetadata;
  indexed_at: string;
  last_refreshed: string;
}
