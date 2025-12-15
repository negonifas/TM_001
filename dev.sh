#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
VENV_DIR="$BACKEND_DIR/.wsl_venv"

if [ ! -f "$VENV_DIR/bin/activate" ]; then
  echo "Backend venv is missing at $VENV_DIR. Create it before running dev.sh."
  exit 1
fi

echo "Starting backend..."
(
  cd "$BACKEND_DIR"
  source "$VENV_DIR/bin/activate"
  uvicorn app.main:app --reload
) &
BACK_PID=$!

echo "Starting frontend..."
(
  cd "$FRONTEND_DIR"
  npm start
) &
FRONT_PID=$!

trap 'echo "Stopping..."; kill $BACK_PID $FRONT_PID 2>/dev/null || true' INT TERM

wait $BACK_PID $FRONT_PID
