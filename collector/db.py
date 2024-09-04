from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point, InfluxDBClient
import random
import time

class InfluxDB:
    def __init__(self, bucket: str, org: str, token: str, url: str):
        self.bucket = bucket
        self.org = org
        self.token = token
        self.url = url
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write_api.close()
        self.client.close()
        self.client = None
        self.write_api = None

    def write(self, project: str, tagkey: str, tagvalue: str, field: str, value):
        # p = influxdb_client.Point("Project").tag("sensor", "FT101").field("value", 25.3)
        if self.client is None:
            raise Exception("This method can only be used in the context of this class (aka use 'with')")
        self.write_api.write(bucket=self.bucket, record=Point(project).tag(tagkey, tagvalue).field(field, value))



if __name__ == "__main__":
    class Cfg:
        bucket = "TestBucket"
        org = "TestOrg"
        token = "abc123!?-"
        url = "http://influxdb:8086"
        project = "Project"
        tagkey = "sensors"
        tagvalue = "FT101"
        field = "value"
        value = lambda _: random.randrange(0, 60)

    cfg = Cfg()

    time.sleep(10)

    with InfluxDB(cfg.bucket, cfg.org, cfg.token, cfg.url) as db:
        for _ in range(360):

            db.write(cfg.project, cfg.tagkey, cfg.tagvalue, cfg.field, cfg.value())
            time.sleep(1)