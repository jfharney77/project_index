import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path

from models import Project, ProjectCreate, ProjectMetadata
from storage import load_projects, get_project, add_project, delete_project, update_project
from analyzer import is_git_repo, analyze_repo, get_readme_content, get_file_tree
from llm import generate_summary
from enrichments.git_remote import get_remote_origin
from enrichments.git_branches import get_branches
from enrichments.llm_improvements import get_improvements

app = FastAPI(title="Project Index API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/projects")
def list_projects():
    return load_projects()


@app.get("/projects/{project_id}")
def get_project_detail(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.post("/projects", status_code=201)
async def create_project(body: ProjectCreate):
    path = body.path.strip()

    if not Path(path).exists():
        raise HTTPException(status_code=400, detail=f"Path does not exist: {path}")

    if not is_git_repo(path):
        raise HTTPException(status_code=400, detail=f"Not a git repository: {path}")

    # Check for duplicates
    existing = load_projects()
    for p in existing:
        if p.path == path:
            raise HTTPException(status_code=409, detail="This repository is already indexed")

    # Analyze
    repo_name = Path(path).name
    metadata = analyze_repo(path)
    metadata.remote_origin = get_remote_origin(path)
    metadata.branches = get_branches(path)
    readme = get_readme_content(path)
    file_tree = get_file_tree(path)

    metadata_summary = (
        f"Total files: {metadata.total_files}, "
        f"Total lines: {metadata.total_lines}, "
        f"Predominant language: {metadata.predominant_language}, "
        f"Languages: {', '.join(l.language for l in metadata.languages[:5])}"
    )

    # Generate AI summary and improvements
    llm_result, improvements = await asyncio.gather(
        generate_summary(repo_name, readme, file_tree, metadata_summary),
        get_improvements(repo_name, readme, file_tree),
    )
    metadata.improvements = improvements

    project = Project(
        name=repo_name,
        path=path,
        summary=llm_result["summary"],
        how_to_run=llm_result["how_to_run"],
        metadata=metadata,
    )

    add_project(project)
    return project


@app.post("/projects/{project_id}/refresh")
async def refresh_project(project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not Path(project.path).exists():
        raise HTTPException(status_code=400, detail="Repository path no longer exists")

    metadata = analyze_repo(project.path)
    metadata.remote_origin = get_remote_origin(project.path)
    metadata.branches = get_branches(project.path)
    readme = get_readme_content(project.path)
    file_tree = get_file_tree(project.path)

    metadata_summary = (
        f"Total files: {metadata.total_files}, "
        f"Total lines: {metadata.total_lines}, "
        f"Predominant language: {metadata.predominant_language}, "
        f"Languages: {', '.join(l.language for l in metadata.languages[:5])}"
    )

    llm_result, improvements = await asyncio.gather(
        generate_summary(project.name, readme, file_tree, metadata_summary),
        get_improvements(project.name, readme, file_tree),
    )

    project.metadata = metadata
    project.metadata.improvements = improvements
    project.summary = llm_result["summary"]
    project.how_to_run = llm_result["how_to_run"]
    project.last_refreshed = datetime.now().isoformat()

    update_project(project)
    return project


@app.delete("/projects/{project_id}", status_code=204)
def remove_project(project_id: str):
    if not delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return None
