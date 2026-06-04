from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def dashboard():

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SVG Digital Twin</title>
        <style>
            body { background: #1e1e1e; color: white; font-family: Arial; }
            svg { background: #2e2e2e; border-radius: 10px; }
            text { fill: white; font-size: 14px; }
        </style>
    </head>
    <body>

        <h1>🏭 Digital Twin (Live)</h1>

        <svg width="800" height="300">

            <!-- Mixer -->
            <rect id="Mixer01" x="50" y="100" width="120" height="80" rx="10" fill="#555"/>
            <text x="70" y="95">Mixer01</text>

            <!-- Conveyor -->
            <rect id="Conveyor03" x="300" y="110" width="160" height="60" rx="10" fill="#555"/>
            <text x="320" y="100">Conveyor03</text>

            <!-- Oven -->
            <rect id="Oven02" x="560" y="100" width="120" height="80" rx="10" fill="#555"/>
            <text x="580" y="95">Oven02</text>

            <!-- Flow lines -->
            <line id="flow1" x1="170" y1="140" x2="300" y2="140" stroke="#444" stroke-width="6"/>
            <line id="flow2" x1="460" y1="140" x2="560" y2="140" stroke="#444" stroke-width="6"/>

        </svg>

        <script>
            function getColor(state) {
                if (state === "READY") return "#4CAF50";
                if (state === "WAITING") return "#FFC107";
                if (state === "TIMEOUT") return "#F44336";
                if (state === "BLOCKED") return "#9E9E9E";
                return "#555";
            }

            function connect() {
                const ws = new WebSocket("ws://127.0.0.1:8000/ws");

                ws.onopen = () => console.log("✅ Connected");

                ws.onmessage = function(event) {

                    const data = JSON.parse(event.data);

                    for (const machine in data) {
                        const el = document.getElementById(machine);

                        if (el) {
                            el.setAttribute("fill", getColor(data[machine].state));
                        }
                    }

                    // Flow coloring
                    if (data["Mixer01"]?.state === "READY") {
                        document.getElementById("flow1").setAttribute("stroke", "#00FF00");
                    } else {
                        document.getElementById("flow1").setAttribute("stroke", "#444");
                    }

                    if (data["Conveyor03"]?.state === "READY") {
                        document.getElementById("flow2").setAttribute("stroke", "#00FF00");
                    } else {
                        document.getElementById("flow2").setAttribute("stroke", "#444");
                    }
                };

                ws.onclose = () => {
                    console.log("🔄 Reconnecting...");
                    setTimeout(connect, 2000);
                };

                ws.onerror = (e) => console.log("❌ WS error", e);
            }

            connect();
        </script>

    </body>
    </html>
    """

    return html