from typing import Dict, Any
import asyncio
from asyncio.events import AbstractEventLoop
from pyspark.sql import SparkSession

from airflow import __version__ as airflow_version

from airflow.hooks.base import BaseHook

from airflow.exceptions import AirflowException

from urllib.parse import urljoin

from requests import exceptions as requests_exceptions

from ocean_spark.response import ApiResponse

from ocean_spark.connect.inverse_websockify import Proxy
import threading

API_HOST = "wss://api.spotinst.io/ocean/spark/"
FE_HOST = "https://console.spotinst.com/ocean/spark/"

USER_AGENT_HEADER = {"user-agent": f"airflow-{airflow_version}"}

DEFAULT_CONN_NAME = "ocean_spark_default"


class OceanSparkConnectHook(BaseHook):
    conn_name_attr: str = "ocean_spark_connect_conn_id"
    default_conn_name: str = "ocean_spark_connect_default"
    conn_type: str = "ocean_spark_connect"
    hook_name: str = "Ocean for Apache Spark (Spark Connect)"

    def __init__(
        self,
        ocean_spark_connect_conn_id: str = "ocean_spark_connect_default",
        sql: str = "select 1",
    ):
        super().__init__()
        self.conn_id = ocean_spark_connect_conn_id
        self.conn = self.get_connection(ocean_spark_connect_conn_id)
        self.token = self.conn.password
        self.cluster_id = self.conn.host
        self.account_id = self.conn.login
        self.app_id = self.conn.port
        self.sql = sql
        self.spark = SparkSession.builder.remote("sc://localhost").getOrCreate()

    def inverse_websockify(self, url: str, loop: AbstractEventLoop) -> None:
        proxy = Proxy(url, self.token)
        loop.run_until_complete(proxy.start())
        loop.run_forever()

    def execute(self, sql: str) -> None:
        path = urljoin(
            API_HOST,
            f"cluster/{self.cluster_id}/app/{self.app_id}/connect?accountId={self.account_id}",
        )

        loop = asyncio.get_event_loop()
        my_thread = threading.Thread(target=self.inverse_websockify, args=(path, loop))
        my_thread.start()

        try:
            self.spark.sql(sql).show()
        except Exception as e:
            self.log.error(e)
            raise AirflowException(e)
        finally:
            loop.stop()
            my_thread.join()

    def kill_task(self) -> None:
        self.spark.stop()

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
