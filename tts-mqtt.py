import os
import time
import subprocess
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "127.0.0.1")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "home/speaker/tts")
TTS_LANG = os.getenv("LANG", "en")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"❌ Failed to connect. Code: {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"🗣️  Received message: {message}")
    try:
        subprocess.run(["espeak", "-v", TTS_LANG, message])
    except Exception as e:
        print(f"❌ TTS failed: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Retry loop
while True:
    try:
        print(f"🔌 Connecting to {MQTT_HOST}:{MQTT_PORT}...")
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        break  # success
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("🔁 Retrying in 5 seconds...")
        time.sleep(5)

# Run MQTT loop
client.loop_forever()
