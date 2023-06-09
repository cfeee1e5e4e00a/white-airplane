""""""
from time import sleep
from datetime import datetime
from typing import List, Dict
from redis import StrictRedis
from influxdb_client import InfluxDBClient, WritePrecision, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from paho.mqtt.client import Client

from src.models.sensor_state import *
from src.env import env

MQTT_BROKER = env["MQTT_BROKER"]
MQTT_PORT = int(env["MQTT_PORT"])
MQTT_PORT = int(env["MQTT_PORT"])


SENSOR_SCHEMAS: List[str] = [
    '{{"house": {house_id},"flat": {flat_id},"value": {value},}}',
    '{{"house": {house_id},"flat": {flat_id},"value": {value},}}',
    '{{"house": {house_id},"flat": {flat_id},"value": {value},}}',
    '{{"supply": {supply_id},"position": "{inout}","value": {value},}}',
]

SENSOR_TOPICS: List[str] = [
    "sensors/humidity",
    "sensors/temperature",
    "sensors/current",
    "sensors/supply/current",
]

SENSOR_DATACLASSES: List[SensorData] = [
    FlatCurrent,
    FlatHumidity,
    FlatTemperature,
    PowerSupplyCurrent,
]

TOPIC2CLASS: Dict[str, SensorData] = {
    topic: cls for topic, cls in zip(SENSOR_TOPICS, SENSOR_DATACLASSES)
}


class SensorsAggregator:
    """Entity subscribed to sensor data topic."""

    def __init__(self, redis: StrictRedis, influx: InfluxDBClient) -> None:
        """"""
        self.redis = redis
        self.influx = influx

        self.mqtt = Client("sensors-aggregator")

        self.transfering: bool = False

        self.mqtt = Client("sensors-aggregator")
        self.mqtt.on_connect = self.__on_connect
        self.mqtt.on_message = self.__on_message
        self.mqtt.connect(host=env["MQTT_BROKER"], port=int(env["MQTT_PORT"]))
        self.mqtt.connect(host=env["MQTT_BROKER"], port=int(env["MQTT_PORT"]))
        self.mqtt.loop_start()

    def stop(self):
        sleep(4)
        self.kill()

    def kill(self):
        self.mqtt.loop_stop()
        for t in SENSOR_TOPICS:
            self.mqtt.unsubscribe(t)
        self.mqtt.disconnect()

    def __on_message(self, client, userdata, msg):
        self.transfering = True
        topic = msg.topic
        msg = str(msg.payload.decode("utf-8"))
        sensor_data = sensor_data_from_str(TOPIC2CLASS[topic], msg)

        print(str(sensor_data), ":", sensor_data.value)
        self.transfering = False

        self.redis.set(str(sensor_data), sensor_data.value)

        p = (
            Point("sensors_logs")
            .tag("type", str(sensor_data))
            .field("value", sensor_data.value)
            .time(datetime.utcnow(), WritePrecision.MS)
        )

        with self.influx.write_api(write_options=SYNCHRONOUS) as write_api:
            write_api.write(bucket="logs", record=p)

        print(f"{str(sensor_data)} = {sensor_data.value}")

    def __on_connect(self, client, userdata, flags, rc):
        for t in SensorsAggregator.SENSOR_TOPICS:
            client.subscribe(t)

    # def __on_message(self, cls):
    #     """"""
    #     def callback(client, userdata, msg):
    #         """"""
    #         msg = str(msg.payload.decode("utf-8"))
    #         sensor_data = sensor_data_from_str(cls, msg)

    #         print(str(sensor_data), ":", sensor_data.value)

    #         self.redis.set(str(sensor_data), sensor_data.value)
    #         #TODO: influx gazfuck sturmentrahen dotabase2

    #     return callback
    def __on_connect(self, client: Client, userdata, flags, rc):
        for t in SENSOR_TOPICS:
            client.subscribe(t, qos=2)
