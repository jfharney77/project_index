import os
import subprocess
from pathlib import Path
from collections import defaultdict

from models import ProjectMetadata, LanguageStats

EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C",
    ".hpp": "C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".r": "R",
    ".R": "R",
    ".sql": "SQL",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".less": "LESS",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".dart": "Dart",
    ".lua": "Lua",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".xml": "XML",
    ".md": "Markdown",
    ".toml": "TOML",
    ".ini": "INI",
    ".cfg": "INI",
    ".dockerfile": "Docker",
    ".tf": "Terraform",
    ".hcl": "HCL",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".zig": "Zig",
    ".nim": "Nim",
    ".pl": "Perl",
    ".pm": "Perl",
}

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".env", "dist", "build", ".next", ".nuxt", "target", "vendor",
    ".idea", ".vscode", "coverage", ".tox", "eggs", "*.egg-info",
}


def is_git_repo(path: str) -> bool:
    git_dir = Path(path) / ".git"
    return git_dir.exists()


def get_git_info(path: str) -> dict:
    info = {
        "last_commit_date": None,
        "default_branch": "",
        "num_commits": 0,
        "num_contributors": 0,
    }
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI"],
            cwd=path, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            info["last_commit_date"] = result.stdout.strip()

        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=path, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            info["default_branch"] = result.stdout.strip()

        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=path, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            info["num_commits"] = int(result.stdout.strip())

        result = subprocess.run(
            ["git", "shortlog", "-sn", "--all"],
            cwd=path, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            info["num_contributors"] = len(result.stdout.strip().splitlines())
    except Exception:
        pass

    return info


def count_lines(filepath: Path) -> int:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def analyze_repo(path: str) -> ProjectMetadata:
    repo_path = Path(path)
    lang_files: defaultdict[str, int] = defaultdict(int)
    lang_lines: defaultdict[str, int] = defaultdict(int)
    total_files = 0
    total_lines = 0
    total_size = 0

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for fname in files:
            fpath = Path(root) / fname
            ext = fpath.suffix.lower()

            if ext in EXTENSION_MAP:
                lang = EXTENSION_MAP[ext]
                lines = count_lines(fpath)
                lang_files[lang] += 1
                lang_lines[lang] += lines
                total_lines += lines
                total_files += 1
                try:
                    total_size += fpath.stat().st_size
                except OSError:
                    pass

    languages = []
    for lang in sorted(lang_lines, key=lang_lines.get, reverse=True):
        pct = (lang_lines[lang] / total_lines * 100) if total_lines > 0 else 0
        languages.append(LanguageStats(
            language=lang,
            files=lang_files[lang],
            lines=lang_lines[lang],
            percentage=round(pct, 1),
        ))

    predominant = languages[0].language if languages else "Unknown"

    git_info = get_git_info(path)

    return ProjectMetadata(
        total_files=total_files,
        total_lines=total_lines,
        total_size_bytes=total_size,
        languages=languages,
        predominant_language=predominant,
        last_commit_date=git_info["last_commit_date"],
        default_branch=git_info["default_branch"],
        num_commits=git_info["num_commits"],
        num_contributors=git_info["num_contributors"],
    )


def get_readme_content(path: str) -> str:
    repo_path = Path(path)
    for name in ["README.md", "README.rst", "README.txt", "README", "readme.md"]:
        readme = repo_path / name
        if readme.exists():
            try:
                return readme.read_text(encoding="utf-8", errors="ignore")[:5000]
            except Exception:
                pass
    return ""


def get_file_tree(path: str, max_files: int = 50) -> str:
    repo_path = Path(path)
    tree_lines = []
    count = 0

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        rel_root = Path(root).relative_to(repo_path)

        for fname in sorted(files):
            if count >= max_files:
                tree_lines.append("... (truncated)")
                return "\n".join(tree_lines)
            rel_path = rel_root / fname
            tree_lines.append(str(rel_path))
            count += 1

    return "\n".join(tree_lines)
