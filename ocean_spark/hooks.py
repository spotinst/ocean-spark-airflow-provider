import json
from datetime import timedelta
from packaging import version
from typing import Callable, Dict, Any, Tuple


from airflow.hooks.base import BaseHook

from airflow import __version__
from airflow.exceptions import AirflowException

from urllib.parse import urljoin

import requests
import time
from requests import exceptions as requests_exceptions

from ocean_spark.response import ApiResponse

API_HOST = "https://api.spotinst.io/ocean/spark/"
FE_HOST = "https://console.spotinst.com/ocean/spark/"

GET_CLUSTER_ENDPOINT = (
    requests.get,
    urljoin(API_HOST, "cluster/{cluster_id}"),
)

SUBMIT_APP_ENDPOINT = (
    requests.post,
    urljoin(API_HOST, "cluster/{cluster_id}/app"),
)
GET_APP_ENDPOINT = (
    requests.get,
    urljoin(API_HOST, "cluster/{cluster_id}/app/{app_id}"),
)
DELETE_APP_ENDPOINT = (
    requests.delete,
    urljoin(API_HOST, "cluster/{cluster_id}/app/{app_id}"),
)

USER_AGENT_HEADER = {"user-agent": "airflow-{v}".format(v=__version__)}

DEFAULT_CONN_NAME = "ocean_spark_default"

# Pyspark 3.4.0 (that allow spark Connect) is only available from Airflow 2.6.2
if version.parse(__version__) >= version.parse("2.6.2"):
    from ocean_spark.connect.hook import OceanSparkConnectHook  # noqa: F401


class OceanSparkHook(BaseHook):
    conn_name_attr: str = "ocean_spark_conn_id"
    default_conn_name: str = "ocean_spark_default"
    conn_type: str = "ocean_spark"
    hook_name: str = "Ocean for Apache Spark"

    def __init__(
        self,
        ocean_spark_conn_id: str = "ocean_spark_default",
        timeout_seconds: int = 180,
        retry_limit: int = 3,
        retry_delay: timedelta = timedelta(seconds=1.0),
    ):
        super().__init__()
        self.conn_id = ocean_spark_conn_id
        self.conn = self.get_connection(ocean_spark_conn_id)
        self.token = self.conn.password
        self.cluster_id = self.conn.host
        self.timeout_seconds = timeout_seconds
        self.account_id = self.conn.login
        if retry_limit < 1:
            raise ValueError("Retry limit must be greater than equal to 1")
        self.retry_limit = retry_limit
        self.retry_delay = retry_delay

    def _do_api_call(self, method: Callable, endpoint: str, payload: Dict) -> Dict:
        """
        Utility function to perform an API call with retries
        :param endpoint_info: Tuple of method and endpoint
        :type endpoint_info: tuple[string, string]
        :param payload: Parameters for this API call.
        :type payload: dict
        :return: If the api call returns a OK status code,
            this function returns the response in JSON. Otherwise,
            we throw an AirflowException.
        :rtype: dict
        """

        if payload is None:
            payload = {}
        headers = {**USER_AGENT_HEADER, "Authorization": f"Bearer {self.token}"}

        attempt_num = 1
        while True:
            try:
                response = method(
                    endpoint,
                    json=payload,
                    headers=headers,
                    params={"accountId": self.account_id},
                    timeout=self.timeout_seconds,
                )
                response.raise_for_status()
                return response.json()
            except (
                requests_exceptions.ConnectionError,
                requests_exceptions.Timeout,
            ) as e:
                self.log.error(
                    "Request attempt [%d] to the Ocean Spark API failed with reason: %s",
                    attempt_num,
                    str(e),
                )
            except requests_exceptions.RequestException as e:
                msg = self._construct_error_message(e)
                self.log.error(msg)
                raise AirflowException(msg)

            if attempt_num == self.retry_limit:
                raise AirflowException(
                    f"Request to Ocean Spark API failed {self.retry_limit} times. Giving up."
                )

            attempt_num += 1
            time.sleep(self.retry_delay.total_seconds())

    @staticmethod
    def _construct_error_message(ex: requests_exceptions.RequestException) -> str:
        try:
            if ex.response is None:
                return f"Request to the Ocean Spark API failed with error {ex}"
            api_response: ApiResponse = json.loads(ex.response.content)
            request_id = api_response["request"]["id"]
            errors = api_response["response"]["errors"]
            status_code = api_response["response"]["status"]["code"]
            return f"Request '{request_id}' to the Ocean Spark API failed with status '{status_code}' and errors: {errors}"
        except ValueError:
            if ex.response is None:
                return f"Request to the Ocean Spark API failed with error {ex}"
            return f"Request to the Ocean Spark API failed with status '{ex.response.status_code}' and error {ex.response.content.decode('utf-8')}"

    def submit_app(self, payload: Dict) -> str:
        method, path = SUBMIT_APP_ENDPOINT
        response = self._do_api_call(
            method,
            path.format(
                cluster_id=self.cluster_id,
                account_id=self.account_id,
            ),
            payload,
        )
        return response["response"]["items"][0]["id"]

    def get_app(self, app_id: str) -> Dict:
        method, path = GET_APP_ENDPOINT
        response = self._do_api_call(
            method,
            path.format(
                cluster_id=self.cluster_id,
                app_id=app_id,
                account_id=self.account_id,
            ),
            {},
        )
        return response["response"]["items"][0]

    def kill_app(self, app_id: str) -> None:
        method, path = DELETE_APP_ENDPOINT
        self._do_api_call(
            method,
            path.format(
                cluster_id=self.cluster_id,
                app_id=app_id,
                account_id=self.account_id,
            ),
            {},
        )

    def get_app_page_url(self, app_id: str) -> str:
        return urljoin(
            FE_HOST,
            f"apps/clusters/{self.cluster_id}/apps/{app_id}/overview&accountId={self.account_id}",
        )

    def test_connection(self) -> Tuple[bool, str]:
        method, path = GET_CLUSTER_ENDPOINT
        try:
            response = self._do_api_call(
                method,
                path.format(
                    cluster_id=self.cluster_id,
                ),
                {},
            )
            if response["response"]["items"][0]["state"] not in [
                "AVAILABLE",
                "PROGRESSING",
            ]:
                return (
                    False,
                    f"Cluster state is {response['response']['items'][0]['state']}",
                )
            return True, "Connection successful"
        except AirflowException as e:
            return False, str(e)

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        return {
            "hidden_fields": ["port", "extra", "schema"],
            "relabeling": {
                "password": "API token",
                "host": "Cluster id",
                "login": "Account id",
            },
            "placeholders": {
                "host": "ocean spark cluster id",
                "password": "Ocean API token",
                "login": "Ocean Spot account id",
            },
        }

    def get_conn(self) -> Any:
        pass
