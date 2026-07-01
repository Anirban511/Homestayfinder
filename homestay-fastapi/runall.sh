#!/usr/bin/env bash
# ===========================================================================
# HomestayFinder (FastAPI + Next.js) - run both services with one command
# ===========================================================================
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Backend setup"
cd "$ROOT/backend"
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
[ -f .env ] || cp .env.example .env
echo "==> Starting API on http://localhost:8000"
uvicorn app.main:app --reload --port 8000 &
API_PID=$!

echo "==> Frontend setup"
cd "$ROOT/frontend"
[ -d node_modules ] || npm install
[ -f .env.local ] || cp .env.example .env.local
echo "==> Starting web on http://localhost:3000"
npm run dev &
WEB_PID=$!

trap "kill $API_PID $WEB_PID 2>/dev/null" EXIT
wait
