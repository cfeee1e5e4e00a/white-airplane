from influxdb_client import InfluxDBClient

from src.env import env


influx = InfluxDBClient(
    url=env["INFLUX_URL"],
    username=env["INFLUX_USERNAME"],
    password=env["INFLUX_PASSWORD"],
    org=env["INFLUX_ORG"],
)
