/*
  NILM sensor node - ESP32
  Reads analog current-sensor channels and publishes them over MQTT as JSON.

  Libraries (Arduino Library Manager): PubSubClient, ArduinoJson
  Setup: copy secrets.h.example to secrets.h and edit it.

  NOTE: Pins/channel names below are an example. Change them to match your wiring.
*/
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "secrets.h"

const char* DEVICE_ID  = "esp32_cnc_01";
const char* MQTT_TOPIC = "cnc/machine_data";
const unsigned long SAMPLE_INTERVAL_MS = 1000;

// ESP32 ADC1 pins (safe to use with WiFi on)
const int NUM_CH = 6;
const int   PINS[NUM_CH]  = {34, 35, 32, 33, 36, 39};
const char* NAMES[NUM_CH] = {"main1", "main2", "spindle", "coolant", "hydraulic", "aaxis"};

WiFiClient espClient;
PubSubClient mqtt(espClient);
unsigned long lastSample = 0;

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi connected, IP: " + WiFi.localIP().toString());
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT... ");
    bool ok = (strlen(MQTT_USER) > 0)
                ? mqtt.connect(DEVICE_ID, MQTT_USER, MQTT_PASS)
                : mqtt.connect(DEVICE_ID);
    if (ok) Serial.println("connected");
    else { Serial.printf("failed (rc=%d), retry in 2s\n", mqtt.state()); delay(2000); }
  }
}

// Average several readings to reduce noise
float readChannel(int pin) {
  long sum = 0;
  for (int i = 0; i < 20; i++) sum += analogRead(pin);
  return (sum / 20.0) * (3.3 / 4095.0);   // convert to volts
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  connectWiFi();
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  if (millis() - lastSample >= SAMPLE_INTERVAL_MS) {
    lastSample = millis();
    StaticJsonDocument<256> doc;
    doc["device_id"] = DEVICE_ID;
    for (int i = 0; i < NUM_CH; i++) doc[NAMES[i]] = readChannel(PINS[i]);

    char payload[256];
    serializeJson(doc, payload);
    mqtt.publish(MQTT_TOPIC, payload);
    Serial.println(payload);
  }
}
