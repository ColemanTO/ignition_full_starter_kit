import subprocess
import sys
import time

print("🚀 Starting Full System...")

# --- Solver ---
solver = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "solver.app:app", "--reload", "--port", "8000"
])

time.sleep(2)

# --- Dashboard ---
dashboard = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "dashboard.app:app", "--reload", "--port", "8080"
])

time.sleep(2)

# --- Simulation ---
sim = subprocess.Popen([
    sys.executable, "run.py"
])

print("\n✅ Everything running!")
print("Solver:    http://localhost:8000")
print("Dashboard: http://localhost:8080")
print("Press Ctrl+C to stop\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    solver.terminate()
    dashboard.terminate()
    sim.terminate()
    