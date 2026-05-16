#!/usr/bin/env bash
set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_DIR="$REPO_ROOT/.pids"
mkdir -p "$PID_DIR"

# Backend
echo "Starting backend..."
cd "$REPO_ROOT/backend"
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
echo $! > "$PID_DIR/backend.pid"

# Frontend
echo "Starting frontend..."
cd "$REPO_ROOT/frontend"
npm run dev &
echo $! > "$PID_DIR/frontend.pid"

echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Run scripts/stop-all.sh to stop."

wait
