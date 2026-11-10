"""Debug tool: prints every MQTT message so you can check the ESP32 is sending data."""
import paho.mqtt.client as mqtt
import config


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to broker, result:", reason_code)
    client.subscribe(config.MQTT_TOPIC)


def on_message(client, userdata, msg):
    print(f"[{msg.topic}] {msg.payload.decode()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if config.MQTT_USER:
    client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.MQTT_BROKER, config.MQTT_PORT)
client.loop_forever()
