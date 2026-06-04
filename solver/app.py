
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

GLOBAL_STATE = {}
clients = []

# Allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/solve")
async def solve(data: dict):
    global GLOBAL_STATE

    state = data.get("state", {})
    GLOBAL_STATE = state

    schedule = []

    for k, v in state.items():
        if v["state"] == "IDLE":
            schedule.append({"machine": k, "action": "START"})

    # ✅ Broadcast new state to all clients
    await broadcast_state()

    return {"schedule": schedule}


def safe_json(data):
    import datetime

    def convert(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return obj

    return json.dumps(data, default=convert)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("✅ WebSocket connected")

    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            # keep connection alive even if no data changes
            await websocket.send_text(safe_json(GLOBAL_STATE))
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("🛑 Client disconnected")

    except Exception as e:
        print("❌ WebSocket error:", e)

    finally:
        if websocket in clients:
            clients.remove(websocket)


async def broadcast_state():
    dead = []

    for client in clients:
        try:
            await client.send_text(json.dumps(GLOBAL_STATE))
        except:
            dead.append(client)

    # clean dead connections
    for d in dead:
        clients.remove(d)


@app.get("/solve_state")
def get_state():
    return GLOBAL_STATE
