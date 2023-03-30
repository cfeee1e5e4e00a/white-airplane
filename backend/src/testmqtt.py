import asyncio
from time import sleep
from paho.mqtt.client import Client
from env import env


def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("ping")


def on_message(a, b, c):
    print(a, b, c)


mqtt = Client()
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect(host=env['MQTT_BROKER'], port=int(env['MQTT_PORT']))
mqtt.loop_start()
sleep(10)
mqtt.loop_stop()
