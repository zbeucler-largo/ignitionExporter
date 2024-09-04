# from asyncua.sync import Client
# from influxdb_client import InfluxDBClient, Point
# from influxdb_client.client.write_api import SYNCHRONOUS
# import time


# class OPCUAInfluxDBBridge:
#     def __init__(self, opcua_url, node_id, influx_config):
#         self.opcua_url = opcua_url
#         self.node_id = node_id
#         self.influx_client = InfluxDBClient(**influx_config)
#         self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)

#     def run(self):
#         with Client(url=self.opcua_url) as opcua_client:
#             print(f"Connected to OPC UA server at {self.opcua_url}")
#             node = opcua_client.get_node(self.node_id)

#             while True:
#                 try:
#                     value = node.read_value()

#                     point = Point("Project").tag("sensor", "FT101").field("value", value)
#                     self.write_api.write(bucket=self.influx_client.bucket, record=point)
#                     print("Value written to InfluxDB")

#                     time.sleep(1)  # Wait for 1 second before reading again
#                 except Exception as e:
#                     print(f"An error occurred: {e}")
#                     time.sleep(5)  # Wait for 5 seconds before retrying

#     def close(self):
#         self.write_api.close()
#         self.influx_client.close()

# def main():
#     opcua_url = "opc.tcp://localhost:62541"
#     node_id = "[Ignition OPC UA Server]ns=1;s=VendorServerInfo/SystemCpuLoad"

#     influx_config = {
#         'url': "http://localhost:8086",
#         'token': "abc123!?-",
#         'org': "TestOrg",
#         'bucket': "TestBucket",
#     }

#     data = {
#         "project": "Project",
#         "tagname": "sensor",
#         "tagvalue": "FT101",
#         "field": "value",
#     }

#     bridge = OPCUAInfluxDBBridge(opcua_url, node_id, influx_config)
#     try:
#         bridge.run()
#     except KeyboardInterrupt:
#         print("Stopping the bridge...")
#     finally:
#         bridge.close()

# if __name__ == "__main__":
#     time.sleep(60)
#     main()

"""
    opcua_url = "opc.tcp://localhost:62541"
    node_id = "[Ignition OPC UA Server]ns=1;s=VendorServerInfo/SystemCpuLoad"

    influx_config = {
        'url': "http://localhost:8086",
        'token': "abc123!?-",
        'org': "TestOrg",
        'bucket': "TestBucket",
    }

    data = {
        "project": "Project",
        "tagname": "sensor",
        "tagvalue": "FT101",
        "field": "value",
    }
"""

import asyncio
from asyncua import Client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time


class OPCUAInfluxDBBridge:
    def __init__(self, opcua_url, node_id, influx_config, sleep_interval=1):
        self.opcua_url = opcua_url
        self.node_id = node_id
        self.influx_client = InfluxDBClient(**influx_config)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        self.sleep_interval = sleep_interval

    async def run(self):
        async with Client(url=self.opcua_url) as opcua_client:
            print(f"Connected to OPC UA server at {self.opcua_url}")
            node = opcua_client.get_node(self.node_id)

            while True:
                try:
                    value = await node.read_value()
                    print(f"Read value: {value}")

                    point = Point("OPCUAMeasurement").tag("node_id", self.node_id).field("value", value)
                    self.write_api.write(bucket=self.influx_client.bucket, record=point)
                    print("Value written to InfluxDB")

                    await asyncio.sleep(self.sleep_interval)  # Wait for 1 second before reading again
                except Exception as e:
                    print(f"An error occurred: {e}")
                    await asyncio.sleep(5)  # Wait for 5 seconds before retrying

    def close(self):
        self.write_api.close()
        self.influx_client.close()

async def main():
    opcua_url = "opc.tcp://localhost:62541"
    node_id = "[Ignition OPC UA Server]ns=1;s=VendorServerInfo/SystemCpuLoad"

    influx_config = {
        'url': "http://localhost:8086",
        'token': "abc123!?-",
        'org': "TestOrg",
        'bucket': "TestBucket",
    }

    bridge = OPCUAInfluxDBBridge(opcua_url, node_id, influx_config)
    try:
        await bridge.run()
    except KeyboardInterrupt:
        print("Stopping the bridge...")
    finally:
        bridge.close()

if __name__ == "__main__":
    time.sleep(15)
    asyncio.run(main())