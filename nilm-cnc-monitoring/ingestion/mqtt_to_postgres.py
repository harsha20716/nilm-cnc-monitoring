"""Logger: receives MQTT messages from the ESP32 and stores them in TimescaleDB."""
import json
import paho.mqtt.client as mqtt
import psycopg2
import config

COLUMNS = ["main1", "main2", "spindle", "coolant", "hydraulic", "aaxis"]

conn = psycopg2.connect(
    host=config.DB_HOST, port=config.DB_PORT, dbname=config.DB_NAME,
    user=config.DB_USER, password=config.DB_PASS,
)
conn.autocommit = True

INSERT_SQL = (
    "INSERT INTO machine_data (time, device_id, " + ", ".join(COLUMNS) + ") "
    "VALUES (NOW(), %s, " + ", ".join(["%s"] * len(COLUMNS)) + ")"
)


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT broker:", reason_code)
    client.subscribe(config.MQTT_TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        values = [data.get("device_id", "unknown")] + [data.get(c) for c in COLUMNS]
        with conn.cursor() as cur:
            cur.execute(INSERT_SQL, values)
        print("Saved:", data)
    except Exception as e:
        print("Error saving message:", e)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if config.MQTT_USER:
    client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.MQTT_BROKER, config.MQTT_PORT)
client.loop_forever()
