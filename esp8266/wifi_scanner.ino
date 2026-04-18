#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// 🔐 WiFi Credentials
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// 🌐 Your Flask Server URL (IMPORTANT: change if IP changes)
String serverURL = "http://YOUR_SERVER_IP:5000/log";

// 📡 Network Structure
struct Network {
  String ssid;
  String bssid;
  int channel;
  int rssi;
  bool isOpen;
  int risk;
};

Network networks[50];

// 📤 Send data to Flask server
void sendLog(String data) {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ WiFi not connected");
    return;
  }

  WiFiClient client;
  HTTPClient http;

  http.begin(client, serverURL);
  http.addHeader("Content-Type", "application/json");

  int response = http.POST(data);

  Serial.print("🌐 Server Response: ");
  Serial.println(response);

  http.end();
}

// 🧠 SMART RISK DETECTION (EVIL TWIN)
int calculateRisk(String ssid, String bssid, int rssi, int channel) {

  int risk = 0;

  int count = 0;
  int differentBSSID = 0;
  int channelMismatch = 0;

  for (int i = 0; i < 50; i++) {

    if (networks[i].ssid == ssid && networks[i].bssid != "") {

      count++;

      if (networks[i].bssid != bssid) {
        differentBSSID++;
      }

      if (networks[i].channel != channel) {
        channelMismatch++;
      }
    }
  }

  // 🚨 Same SSID + different BSSID
  if (count > 1 && differentBSSID > 0) {
    risk += 3;
  }

  // 🚨 Very strong signal (suspicious nearby attacker)
  if (rssi > -50) {
    risk += 2;
  }

  // 🚨 Channel mismatch
  if (channelMismatch > 0) {
    risk += 1;
  }

  return risk;
}

// 🧠 SETUP
void setup() {

  Serial.begin(115200);
  delay(1000);

  Serial.println("\n🚀 BOOT STARTED");

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.print("Connecting to WiFi");

  WiFi.begin(ssid, password);

  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    attempts++;

    if (attempts > 20) {
      Serial.println("\n❌ WiFi FAILED");
      return;
    }
  }

  Serial.println("\n✅ Connected!");
  Serial.print("📡 IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.localIP());
}

// 🔁 LOOP
void loop() {

  Serial.println("\n==============================");
  Serial.println("🔁 LOOP RUNNING");
  Serial.println("🔍 Scanning WiFi...");

  int n = WiFi.scanNetworks();

  Serial.print("📶 Networks found: ");
  Serial.println(n);

  if (n == 0) {
    Serial.println("❌ No networks found");
    delay(5000);
    return;
  }

  for (int i = 0; i < n && i < 50; i++) {

    networks[i].ssid = WiFi.SSID(i);
    networks[i].bssid = WiFi.BSSIDstr(i);
    networks[i].channel = WiFi.channel(i);
    networks[i].rssi = WiFi.RSSI(i);
    networks[i].isOpen = (WiFi.encryptionType(i) == ENC_TYPE_NONE);

    networks[i].risk = calculateRisk(
      networks[i].ssid,
      networks[i].bssid,
      networks[i].rssi,
      networks[i].channel
    );

    Serial.println("--------------------------------");
    Serial.println("📡 SSID: " + networks[i].ssid);
    Serial.println("🧬 BSSID: " + networks[i].bssid);
    Serial.println("📶 Channel: " + String(networks[i].channel));
    Serial.println("📉 Signal: " + String(networks[i].rssi));
    Serial.println("🔐 Security: " + String(networks[i].isOpen ? "OPEN" : "SECURED"));
    Serial.println("⚠️ Risk Score: " + String(networks[i].risk));

    if (networks[i].risk >= 4) {
      Serial.println("🚨 POSSIBLE EVIL TWIN DETECTED!");
    }

    // 📤 JSON Data
    String json = "{";
    json += "\"ssid\":\"" + networks[i].ssid + "\",";
    json += "\"bssid\":\"" + networks[i].bssid + "\",";
    json += "\"channel\":" + String(networks[i].channel) + ",";
    json += "\"rssi\":" + String(networks[i].rssi) + ",";
    json += "\"risk\":" + String(networks[i].risk);
    json += "}";

    sendLog(json);
  }

  Serial.println("⏳ Waiting 10 seconds...\n");

  delay(10000);
}
