import paho.mqtt.client as mqtt
import ssl
import RPi.GPIO as GPIO
import time

# MQTT config
broker = "53173614eeb446b7bfb4e11af4340b65.s1.eu.hivemq.cloud"
port = 8883
username = "user1"
password = "Username1"
topic = "bracelet/vibe"

# GPIO config
LED_PIN = 25  # GPIO 25 (physical pin 22)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def flash_led():
    for _ in range(2):  # Flash twice
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.3)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to broker")
        client.subscribe(topic)
        print(f"📡 Subscribed to `{topic}`")
    else:
        print("❌ Connection failed, code:", rc)

def on_message(client, userdata, msg):
    print(f"📩 Received on `{msg.topic}`: {msg.payload.decode()}")
    if msg.payload.decode() == "1":
        flash_led()

client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

print("🔌 Connecting...")
client.connect(broker, port, 60)
client.loop_forever()
