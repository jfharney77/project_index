# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev       # dev server at http://localhost:5173
npm run build     # tsc + vite build
```

## Architecture

This is a monorepo with a **FastAPI backend** (`backend/`) and a **React/TypeScript/Vite frontend** (`frontend/`).

**Request flow:** Browser → Vite dev server (`:5173`) → proxy `/projects/*` → FastAPI (`:8000`)

The Vite proxy (`vite.config.ts`) forwards all `/projects` paths to the backend, so `api.ts` uses relative URLs (`/projects`) with no hardcoded port.

### Backend modules

| File | Role |
|---|---|
| `main.py` | FastAPI app, all route handlers (CRUD + refresh) |
| `models.py` | Pydantic models: `ProjectCreate`, `Project`, `ProjectMetadata`, `LanguageStats` |
| `storage.py` | Read/write `data/projects.json` — no database, flat file persistence |
| `analyzer.py` | Walks the repo filesystem, counts LOC by language, runs `git` subprocesses for metadata |
| `llm.py` | Dispatches to Ollama or Cerebras; parses `SUMMARY:` / `HOW TO RUN:` sections from LLM response |

### Frontend components

`App.tsx` owns all state (projects list, selected project). It passes callbacks down to:
- `AddProjectDialog` — form that calls `POST /projects`
- `ProjectCard` — card in the grid; triggers select/delete/refresh
- `ProjectDetail` — full detail view rendered instead of the grid when a project is selected

`api.ts` is the only file that calls `fetch`; all API calls go through it.
`types.ts` mirrors the backend Pydantic models as TypeScript interfaces.

### LLM configuration

Controlled entirely by `backend/.env`. Copy `.env.example` to `.env`.

- `LLM_PROVIDER=ollama` (default) — requires Ollama running locally
- `LLM_PROVIDER=cerebras` — requires `CEREBRAS_API_KEY`

In WSL, set `OLLAMA_BASE_URL=http://172.30.48.1:11434` to reach Ollama on the Windows host (the default already reflects this).

### Data persistence

Projects are stored in `backend/data/projects.json` as a JSON array. `storage.py` loads the whole file on every read and rewrites it on every write — fine for a local tool but not concurrent-safe.
