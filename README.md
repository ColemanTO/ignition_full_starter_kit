# 🏭 Ignition Digital Twin Starter Kit

A modern industrial architecture combining:

- ✅ State machine (Ignition-style logic)
- ✅ External solver (optimization engine)
- ✅ Real-time WebSocket streaming
- ✅ Web-based dashboard (SVG digital twin)
- ✅ Simulation environment

---

# 🚀 Quick Start

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Start the system

```bash
./start.sh
# OR
python start.py
```

## 3. Open dashboard

```
http://localhost:8080
```

---

# 🧠 Architecture Overview

```mermaid
flowchart LR

    subgraph Simulation
        A[run.py\nState Generator]
    end

    subgraph Core Engine
        B[State Store\nproject/state.py]
        C[Engine\nproject/engine.py]
    end

    subgraph Solver Service
        D[FastAPI Solver\nsolver/app.py]
    end

    subgraph Streaming Layer
        E[WebSocket Endpoint\n/ws]
    end

    subgraph Web UI
        F[Dashboard\nHTML + SVG]
    end

    A --> B
    B --> C
    C -->|POST /solve| D
    D -->|Update State| E
    E -->|Push JSON| F
```

---

# 🌐 Deployment Diagram

```mermaid
flowchart TB

    subgraph Local Machine / Server
        subgraph Backend Services
            A[FastAPI Solver\nPort 8000]
            B[WebSocket Stream\n/ws endpoint]
        end

        subgraph Frontend
            C[Dashboard UI\nPort 8080]
        end

        subgraph Runtime
            D[Simulation Engine\nrun.py]
        end
    end

    D -->|POST /solve| A
    A -->|Update State| B
    B -->|Push updates| C
```

---

# 🔁 Data Flow

1. 🔄 Simulation updates machine state  
2. ⚙️ Engine sends state to solver  
3. 🧠 Solver updates global state  
4. 📡 WebSocket streams updates  
5. 🖥️ Dashboard updates SVG  

---

# ✅ Summary

You now have a complete real-time industrial system stack:

- Control logic
- Optimization
- Real-time streaming
- Live visualization
