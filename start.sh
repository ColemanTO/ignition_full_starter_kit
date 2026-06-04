#!/usr/bin/env bash

echo "🚀 Starting Ignition Starter Kit..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $(pwd)"

# Activate venv
if [ -d ".venv" ]; then
  source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate
fi

# Force Python to see this directory
export PYTHONPATH="$SCRIPT_DIR"

# Start Solver
echo "Starting Solver..."
python -m uvicorn solver.app:app --reload --port 8000 --app-dir "$SCRIPT_DIR" &
SOLVER_PID=$!

sleep 2

# Start Dashboard
echo "Starting Dashboard..."
python -m uvicorn dashboard.app:app --reload --port 8080 --app-dir "$SCRIPT_DIR" &
DASHBOARD_PID=$!

sleep 2

# Start Simulation
echo "Starting Simulation..."
python run.py &
SIM_PID=$!

# Open browser
echo "Opening dashboard..."
start http://localhost:8080 2>/dev/null || true

echo ""
echo "✅ System running!"
echo ""

cleanup() {
  echo "🛑 Shutting down..."
  kill $SOLVER_PID 2>/dev/null
  kill $DASHBOARD_PID 2>/dev/null
  kill $SIM_PID 2>/dev/null
  exit 0
}

trap cleanup INT TERM

wait
