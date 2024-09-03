import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Wait for InfluxDB to be ready (if needed)
time.sleep(30)

bucket = "TestBucket"
org = "TestOrg"
token = "abc123!?-"  # Make sure this is the correct token
url = "http://influxdb:8086"

# Create the client
try:
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    logger.info("InfluxDB client created successfully")
except Exception as e:
    logger.error(f"Failed to create InfluxDB client: {e}")
    exit(1)

# Create the write API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Function to write data
def write_data():
    try:
        p = influxdb_client.Point("Project").tag("sensor", "FT101").field("value", 25.3)
        write_api.write(bucket=bucket, record=p)
        logger.info("Data written successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to write data: {e}")
        return False

# Try to write data multiple times
max_retries = 5
for attempt in range(max_retries):
    if write_data():
        break
    else:
        logger.warning(f"Write attempt {attempt + 1} failed. Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying

# Check the health of the InfluxDB instance
try:
    health = client.health()
    logger.info(f"InfluxDB health: {health}")
except Exception as e:
    logger.error(f"Failed to check InfluxDB health: {e}")

# Close the client
client.close()