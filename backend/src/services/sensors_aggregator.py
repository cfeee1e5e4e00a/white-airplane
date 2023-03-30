""""""
from typing import Any, List, Dict
from paho.mqtt import subscribe
from redis import StrictRedis
from paho.mqtt.client import Client

from src.models.sensor_state import *

from src.env import env

MQTT_BROKER = env["MQTT_BROKER"]
MQTT_PORT   = int(env["MQTT_PORT"])

class SensorsAggregator:
    """Entity subscribed to sensor data topic."""

    SENSOR_SCHEMAS: ClassVar[List[str]] = [
        '{{"house": {id},"flat": {id},"value": {value},}}',
        '{{"house": {id},"flat": {id},"value": {value},}}',
        '{{"house": {id},"flat": {id},"value": {value},}}',
        '{{"supply": {id},"position": "{inout}","value": {value},}}',
    ]

    SENSOR_TOPICS: ClassVar[List[str]] = [
        "sensors/humidity",
        "sensors/temperature",
        "sensors/current",
        "sensors/supply/current",
    ]

    __SENSOR_DATACLASSES: ClassVar[List[SensorData]] = [
        FlatCurrent,
        FlatHumidity,
        FlatTemperature,
        SupplyCurrent,
    ]

    __TOPIC2CLASS: ClassVar[Dict[str, SensorData]] = {
        topic: cls for topic, cls in zip(SENSOR_TOPICS, __SENSOR_DATACLASSES)
    }

    def __init__(self, redis) -> None:
        """"""
        self.redis: StrictRedis = redis
        
        self.mqtt = Client('sensors-aggregator')
        self.mqtt.on_connect = self.__on_connect
        self.mqtt.on_message = self.__on_message
        self.mqtt.connect(host=env['MQTT_BROKER'], port=int(env['MQTT_PORT']))
        self.mqtt.loop_start()

    def stop(self):
        self.mqtt.loop_stop()
        for t in SensorsAggregator.SENSOR_TOPICS:
            self.mqtt.unsubscribe(t)
        self.mqtt.disconnect()

    def __on_message(self, client, userdata, msg):
        topic = msg.topic
        msg = str(msg.payload.decode("utf-8"))
        sensor_data = sensor_data_from_str(SensorsAggregator.__TOPIC2CLASS[topic], msg)

        print(str(sensor_data), ":", sensor_data.value)

        self.redis.set(str(sensor_data), sensor_data.value)

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
    #         #TODO: influx gazfuck sturmentrahen

    #     return callback
