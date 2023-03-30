from paho.mqtt.client import Client
from src.env import env

MQTT_BROKER = env["MQTT_BROKER"]
MQTT_PORT = int(env["MQTT_PORT"])


def on_publish(client, userdata, mid):
    """TODO: Logging."""


CLIENT = Client("client")
CLIENT.on_publish = on_publish  # future logging
CLIENT.connect(MQTT_BROKER, MQTT_PORT)
