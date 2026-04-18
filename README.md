# 🚨 WiFi Security IDS (ESP8266 + Flask)

A real-time WiFi Intrusion Detection System that scans nearby networks and detects suspicious behavior such as **Evil Twin attacks** using BSSID and signal analysis.

---

## 📌 Project Overview

This system consists of two parts:

1. **ESP8266 (NodeMCU)**

   * Scans nearby WiFi networks
   * Extracts SSID, BSSID, channel, RSSI
   * Calculates risk score
   * Sends data to server

2. **Flask Server (Python)**

   * Receives data via HTTP
   * Stores logs
   * Displays dashboard
   * Shows alerts and risk graph

---

## ⚙️ Setup Instructions

### 🖥️ 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/wifi-security-ids.git
cd wifi-security-ids
```

---

### 📡 2. Setup ESP8266 (Arduino)

Open file:

```text
esp8266/wifi_scanner.ino
```

Update these values:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

String serverURL = "http://YOUR_LAPTOP_IP:5000/log";
```

---

### 🌐 3. Find Your Laptop IP

Run on Ubuntu:

```bash
ip a
```

Look for:

```text
inet 192.168.X.X
```

Example:

```text
192.168.1.21
```

Use it like:

```cpp
http://192.168.1.21:5000/log
```

---

### 🧠 4. Setup Python Server

Go to server folder:

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install flask
```

Run server:

```bash
python3 server.py
```

You should see:

```text
Running on http://0.0.0.0:5000
Running on http://192.168.X.X:5000
```

---

### 🔌 5. Upload Code to ESP8266

* Open Arduino IDE
* Select board: NodeMCU (ESP8266)
* Select correct port
* Upload code

---

### 📊 6. Open Dashboard

In browser:

```text
http://YOUR_LAPTOP_IP:5000
```

---

## 🚨 Detection Logic

The system flags suspicious networks based on:

* Same SSID + different BSSID
* Strong signal strength (possible nearby attacker)
* Channel mismatch

Risk scoring:

* +3 → Multiple BSSID for same SSID
* +2 → Very strong signal
* +1 → Channel mismatch

---

## 🧪 Example Scenario

If a fake hotspot mimics your WiFi name:

```text
SSID: Airtel_ADITYA
BSSID: Different
```

➡️ System detects it as **possible Evil Twin attack**

---

## 📁 Project Structure

```text
wifi-security-ids/
├── esp8266/
│   └── wifi_scanner.ino
├── server/
│   └── server.py
├── README.md
└── .gitignore
```

---

## ⚠️ Important Notes

* ESP8266 works only on **2.4 GHz networks**
* Laptop and ESP must be on **same WiFi network**
* Firewall should not block port **5000**

---

## 🚀 Future Scope

* ESP32 support (5 GHz scanning)
* Machine learning-based detection
* Email/SMS alerts
* Cloud deployment

---

## 👨‍💻 Author

Aditya Khandelwal
B.Tech CSE (Cyber Security)
SOC Analyst Aspirant
