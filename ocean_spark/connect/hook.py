from multiprocessing import Process
from typing import Dict, Any
import grpc  # type: ignore
from pyspark.sql.connect.session import SparkSession
from pyspark.sql.connect.client import ChannelBuilder

from airflow import __version__ as airflow_version

from airflow.hooks.base import BaseHook

from airflow.exceptions import AirflowException

from urllib.parse import urljoin

from ocean_spark.connect.inverse_websockify import Proxy

API_HOST = "wss://api.spotinst.io/ocean/spark/"
FE_HOST = "https://console.spotinst.com/ocean/spark/"

USER_AGENT_HEADER = {"user-agent": f"airflow-{airflow_version}"}

DEFAULT_CONN_NAME = "ocean_spark_connect_default"


class OceanChannelBuilder(ChannelBuilder):
    def __init__(self, url: str, bind_address: str):
        super().__init__(url)
        self._bind_address = bind_address

    def toChannel(self) -> grpc.Channel:
        if self._bind_address.startswith("/"):
            channel = grpc.insecure_channel("unix:" + self._bind_address)
        else:
            channel = super().toChannel()
        return channel


class OceanSparkConnectHook(BaseHook):
    conn_name_attr: str = "ocean_spark_connect_conn_id"
    default_conn_name: str = "ocean_spark_connect_default"
    conn_type: str = "ocean_spark_connect"
    hook_name: str = "Ocean for Apache Spark (Spark Connect)"

    def __init__(
        self,
        ocean_spark_connect_conn_id: str = "ocean_spark_connect_default",
    ):
        super().__init__()
        self.conn_id = ocean_spark_connect_conn_id
        self.conn = self.get_connection(ocean_spark_connect_conn_id)
        self.token = self.conn.password
        self.cluster_id = self.conn.host
        self.account_id = self.conn.login
        self.app_id = self.conn.schema

    def execute(self, sql: str) -> None:
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
            self.log.info(f"Executing SQL: {sql}")
            spark.sql(sql).show()
            self.log.info("SQL executed successfully")
        except Exception as e:
            self.log.error(e)
            raise AirflowException(e)
        finally:
            self.log.info("Stopping Spark session")
            spark.stop()
            _process.kill()
            self.log.info("Job done")

    def kill_task(self) -> None:
        pass

    def get_app_page_url(self) -> str:
        url = urljoin(
            FE_HOST,
            f"apps/clusters/{self.cluster_id}/apps/{self.app_id}/overview&accountId={self.account_id}",
        )
        return url

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        return {
            "hidden_fields": ["extra", "port"],
            "relabeling": {
                "password": "API token",
                "host": "Cluster id",
                "login": "Account id",
                "schema": "Application Id",
            },
            "placeholders": {
                "host": "ocean spark cluster id",
                "password": "Ocean API token",
                "login": "Ocean Spot account id",
                "schema": "Ocean Spark Application Id",
            },
        }

    def get_conn(self) -> Any:
        pass
