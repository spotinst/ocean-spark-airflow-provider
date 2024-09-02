import asyncio

from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.utils import timezone

from ocean_spark.connect.inverse_websockify import Proxy

class SparkConnectTrigger(BaseTrigger):
    def __init__(self, sql):
        super().__init__()
        self.sql = sql

    def serialize(self):
        return ("ocean_spark.connect.spark_connect_trigger.SparkConnectTrigger", {"sql": self.sql})
    
    async def run(self):
        proxy = Proxy(args.url, args.token, args.port, args.listen)
        loop.run_until_complete(proxy.start())
        loop.run_forever()
        while self.sql > timezone.utcnow():
            await asyncio.sleep(1)
        yield TriggerEvent(self.sql)