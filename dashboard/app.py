from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def dashboard():

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Digital Twin</title>
        <style>
            body { font-family: Arial; background: #1e1e1e; color: white; }
            .container { display: flex; flex-wrap: wrap; }
            .card {
                margin: 10px;
                padding: 15px;
                border-radius: 8px;
                width: 200px;
                transition: 0.3s;
            }
            .READY { background: #2e7d32; }
            .WAITING { background: #f9a825; }
            .TIMEOUT { background: #c62828; }
            .IDLE { background: #555; }
        </style>
    </head>
    <body>

        <h1>🏭 Real-Time Dashboard</h1>
        <div id="machines" class="container"></div>

        <script>
            const container = document.getElementById("machines");

            const ws = new WebSocket("ws://localhost:8000/ws");

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);

                container.innerHTML = "";

                for (const machine in data) {
                    const m = data[machine];
                    const div = document.createElement("div");

                    const state = m.state || "UNKNOWN";

                    div.className = "card " + state;

                    div.innerHTML = `
                        <h3>${machine}</h3>
                        <p>State: ${state}</p>
                        <p>Status: ${m.status}</p>
                    `;

                    container.appendChild(div);
                }
            };

            ws.onopen = () => console.log("✅ Connected to live stream");
            ws.onerror = (e) => console.error("❌ WebSocket error", e);
        </script>

    </body>
    </html>
    """

    return html