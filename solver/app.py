
from fastapi import FastAPI, WebSocket
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except:
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
