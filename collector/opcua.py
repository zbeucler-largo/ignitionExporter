# import random
# import asyncio
# from asyncua import Client

# sleep_interval = 1

# class Cfg:
#     bucket = "TestBucket"
#     org = "TestOrg"
#     token = "abc123!?-"
#     url = "http://influxdb:8086"
#     project = "Project"
#     tagkey = "sensors"
#     tagvalue = "test"
#     field = "value"
#     value = lambda _: random.randrange(0, 60)

# async def main():
#     opcua_url = "opc.tcp://localhost:62541"    
#     node_id = "[Ignition OPC UA Server]ns=0;i=2258" # current time

#     db_cfg = Cfg()

#     try:
#         async with Client(url=opcua_url) as client:
#             print(f"Connected to OPC UA server at {opcua_url}")
#             node = client.get_node(node_id)
#             value = await node.read_value()
#             print(f"Value of node {node_id}: {value}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     asyncio.run(main())


from asyncua.sync import Client
from db import InfluxDB


