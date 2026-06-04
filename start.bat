@echo off
echo Starting Ignition Starter Kit...

start cmd /k "uvicorn solver.app:app --reload"
timeout /t 2 >nul
start cmd /k "python run.py"

echo System started!
pause
