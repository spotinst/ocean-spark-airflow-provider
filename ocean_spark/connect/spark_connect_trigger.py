from multiprocessing import Process
from typing import AsyncGenerator

from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.exceptions import AirflowException
from urllib.parse import urljoin

from pyspark.sql.connect.session import SparkSession
from ocean_spark.connect.hook import OceanChannelBuilder

from ocean_spark.connect.inverse_websockify import Proxy

from ocean_spark.connect.hook import API_HOST


class SparkConnectTrigger(BaseTrigger):
    def __init__(
        self, sql: str, token: str, cluster_id: str, account_id: str, app_id: str
    ):
        super().__init__()
        self.sql = sql
        self.token = token
        self.cluster_id = cluster_id
        self.account_id = account_id
        self.app_id = app_id

    def serialize(self) -> tuple[str, dict[str, str]]:
        return "ocean_spark.connect.spark_connect_trigger.SparkConnectTrigger", {
            "sql": self.sql,
            "token": self.token,
            "cluster_id": self.cluster_id,
            "account_id": self.account_id,
            "app_id": self.app_id,
        }

    async def run(self) -> AsyncGenerator[TriggerEvent, None]:
        path = urljoin(
            API_HOST,
            f"cluster/{self.cluster_id}/app/{self.app_id}/connect?accountId={self.account_id}",
        )

        self.log.info(f"Starting inverse websockify {path}")
        _proxy = Proxy(path, self.token, -1, "0.0.0.0", -1)
        _process = Process(target=_proxy.inverse_websockify, args=())
        _process.start()

        self.log.info(f"Starting Spark session on {_proxy.addr}")
        channel_builder = OceanChannelBuilder(
            f"sc://localhost:{_proxy.port}", _proxy.addr
        )
        spark = SparkSession.Builder().channelBuilder(channel_builder).getOrCreate()
        try:
            self.log.info(f"Executing SQL: {self.sql}")
            spark.sql(self.sql).show()
            self.log.info("SQL executed successfully")
        except Exception as e:
            self.log.error(e)
            raise AirflowException(e)
        finally:
            self.log.info("Stopping Spark session")
            spark.stop()
            _process.kill()
            self.log.info("Job done")

        yield TriggerEvent(self.sql)
