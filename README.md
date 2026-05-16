# Project Index

A local web application that indexes your git repositories and provides AI-generated summaries, run instructions, and code metrics.

## Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.ai/) running locally with a model pulled (default: `llama3`)

## Quick Start

### 1. Start Ollama

```bash
ollama serve
ollama pull llama3
```

### 2. Install dependencies

```bash
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd frontend && npm install
```

### 3. Start the app

```bash
./scripts/run-all.sh
```

The app will be available at **http://localhost:5173**

To stop:

```bash
./scripts/stop-all.sh
```

#### Run services individually

```bash
./scripts/run-backend.sh   # FastAPI on :8000
./scripts/run-frontend.sh  # Vite dev server on :5173
```

## Usage

1. Open the app in your browser
2. Click "Add Project" and paste the absolute path to any local git repository
3. The app will analyze the repo (file count, LOC, languages) and generate an AI summary via Ollama
4. View the dashboard to browse all indexed projects

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3` | Model to use for summaries |

## Tech Stack

- **Frontend**: React, TypeScript, Vite, TailwindCSS, Lucide icons
- **Backend**: FastAPI, Python, httpx
- **AI**: Ollama (local LLM)
- **Storage**: JSON file
