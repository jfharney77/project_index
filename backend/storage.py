import json
import os
from pathlib import Path
from typing import Optional

from models import Project

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "projects.json"


def _ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps([], indent=2))


def load_projects() -> list[Project]:
    _ensure_data_file()
    raw = json.loads(DATA_FILE.read_text())
    return [Project(**p) for p in raw]


def save_projects(projects: list[Project]):
    _ensure_data_file()
    DATA_FILE.write_text(
        json.dumps([p.model_dump() for p in projects], indent=2)
    )


def get_project(project_id: str) -> Optional[Project]:
    projects = load_projects()
    for p in projects:
        if p.id == project_id:
            return p
    return None


def add_project(project: Project) -> Project:
    projects = load_projects()
    projects.append(project)
    save_projects(projects)
    return project


def delete_project(project_id: str) -> bool:
    projects = load_projects()
    filtered = [p for p in projects if p.id != project_id]
    if len(filtered) == len(projects):
        return False
    save_projects(filtered)
    return True


def update_project(project: Project) -> Project:
    projects = load_projects()
    for i, p in enumerate(projects):
        if p.id == project.id:
            projects[i] = project
            break
    save_projects(projects)
    return project
