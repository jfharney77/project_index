from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ProjectCreate(BaseModel):
    path: str = Field(..., description="Absolute path to the local git repository")


class LanguageStats(BaseModel):
    language: str
    files: int
    lines: int
    percentage: float


class ProjectMetadata(BaseModel):
    total_files: int = 0
    total_lines: int = 0
    total_size_bytes: int = 0
    languages: list[LanguageStats] = []
    predominant_language: str = ""
    last_commit_date: Optional[str] = None
    default_branch: str = ""
    num_commits: int = 0
    num_contributors: int = 0
    remote_origin: Optional[str] = None
    branches: Optional[list[str]] = None
    improvements: Optional[list[str]] = None


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    path: str
    summary: str = ""
    how_to_run: str = ""
    metadata: ProjectMetadata = Field(default_factory=ProjectMetadata)
    indexed_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_refreshed: str = Field(default_factory=lambda: datetime.now().isoformat())
