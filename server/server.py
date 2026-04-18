from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json
from collections import Counter

app = Flask(__name__)

logs = []
attacks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>WiFi Security Dashboard</title>
<meta http-equiv="refresh" content="3">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background: #0d1117;
    color: #c9d1d9;
    padding: 20px;
}

h1 {
    color: #00ffe0;
    text-align: center;
}

h2 {
    margin-top: 30px;
    color: #58a6ff;
}

.alert {
    background: #ff0033;
    padding: 15px;
    text-align: center;
    font-weight: bold;
    border-radius: 8px;
    margin-bottom: 20px;
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0.6; }
}

.card {
    background: #161b22;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.stat {
    display: inline-block;
    width: 23%;
    background: #21262d;
    padding: 15px;
    margin: 1%;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}

.safe { color: #00ff88; }
.danger { color: #ff4d4d; }

table {
    width: 100%;
    border-collapse: collapse;
}

th { background: #161b22; padding: 10px; }
td { padding: 8px; text-align: center; }
tr:nth-child(even) { background: #161b22; }

canvas {
    background: white;
    border-radius: 10px;
}
</style>
</head>

<body>

<h1>🛰️ WiFi Security Dashboard</h1>

{% if alert %}
<div class="alert">🚨 AI DETECTED SUSPICIOUS NETWORK 🚨</div>
{% endif %}

<div class="card">
<h2>📊 Stats</h2>

<div class="stat">Logs<br>{{ total_logs }}</div>
<div class="stat">Attacks<br>{{ total_attacks }}</div>
<div class="stat">Top Target<br>{{ top_ssid }}</div>
<div class="stat">Last Attack<br>{{ last_attack }}</div>

</div>

<div class="card">
<h2>📈 Risk Graph</h2>
<canvas id="chart"></canvas>
</div>

<div class="card">
<h2>📶 Live Networks</h2>
<table>
<tr>
<th>SSID</th><th>BSSID</th><th>Channel</th><th>Signal</th><th>Risk</th><th>Time</th>
</tr>
{% for log in logs %}
<tr class="{{ 'danger' if log.risk >= 4 else 'safe' }}">
<td>{{ log.ssid }}</td>
<td>{{ log.bssid }}</td>
<td>{{ log.channel }}</td>
<td>{{ log.rssi }}</td>
<td>{{ log.risk }}</td>
<td>{{ log.time }}</td>
</tr>
{% endfor %}
</table>
</div>

<script>
const labels = {{ times | safe }};
const data = {{ risks | safe }};

new Chart(document.getElementById("chart"), {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "Risk Level",
            data: data,
            borderWidth: 2,
            tension: 0.3
        }]
    }
});
</script>

</body>
</html>
"""

# 🤖 AI Detection Function
def ai_detect():
    if len(logs) < 5:
        return False

    recent = logs[-10:]

    # Pattern 1: same SSID many times
    ssids = [l["ssid"] for l in recent]
    count = Counter(ssids)
    if any(v >= 3 for v in count.values()):
        return True

    # Pattern 2: sudden signal jump
    rssis = [l["rssi"] for l in recent]
    if max(rssis) - min(rssis) > 40:
        return True

    return False


@app.route("/")
def index():
    alert = ai_detect()

    recent = logs[-30:]

    # Graph logic
    risks = []
    times = []

    for i in range(0, len(recent), 3):
        chunk = recent[i:i+3]
        if chunk:
            risks.append(max([l["risk"] for l in chunk]))
            times.append(chunk[-1]["time"])

    # Stats
    total_logs = len(logs)
    total_attacks = len(attacks)

    top_ssid = "N/A"
    if attacks:
        top_ssid = Counter([a["ssid"] for a in attacks]).most_common(1)[0][0]

    last_attack = attacks[-1]["time"] if attacks else "N/A"

    return render_template_string(
        HTML,
        logs=recent,
        alert=alert,
        times=times,
        risks=risks,
        total_logs=total_logs,
        total_attacks=total_attacks,
        top_ssid=top_ssid,
        last_attack=last_attack
    )


@app.route("/log", methods=["POST"])
def log():
    data = request.json
    data["time"] = datetime.now().strftime("%H:%M:%S")

    logs.append(data)

    with open("logs.txt", "a") as f:
        f.write(json.dumps(data) + "\\n")

    if data["risk"] >= 4:
        attacks.append(data)
        print("🚨 ATTACK:", data)
    else:
        print("📥", data)

    return jsonify({"status": "ok"})


app.run(host="0.0.0.0", port=5000)
