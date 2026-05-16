#!/usr/bin/env bash
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_DIR="$REPO_ROOT/.pids"

stop_pid() {
  local name=$1
  local file="$PID_DIR/$name.pid"
  if [ -f "$file" ]; then
    local pid
    pid=$(cat "$file")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" && echo "Stopped $name (pid $pid)"
    else
      echo "$name was not running"
    fi
    rm -f "$file"
  else
    echo "No PID file for $name — killing by port"
    case $name in
      backend)  lsof -ti tcp:8000 | xargs -r kill ;;
      frontend) lsof -ti tcp:5173 | xargs -r kill ;;
    esac
  fi
}

stop_pid backend
stop_pid frontend
