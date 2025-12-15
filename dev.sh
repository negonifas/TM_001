#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

echo "Starting backend..."
(cd backend && source .linux_venv/bin/activate && uvicorn app.main:app --reload) &
BACK_PID=$!

echo "Starting frontend..."
(cd frontend && npm start) &
FRONT_PID=$!

trap 'echo "Stopping..."; kill $BACK_PID $FRONT_PID 2>/dev/null || true' INT TERM

wait $BACK_PID $FRONT_PID
