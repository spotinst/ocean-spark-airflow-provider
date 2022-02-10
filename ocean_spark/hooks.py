from datetime import timedelta
from typing import Callable, Dict
from airflow import __version__ as airflow_version

if airflow_version.startswith("1."):
    from airflow.hooks.base_hook import BaseHook
else:
    from airflow.hooks.base import BaseHook

from airflow import __version__
from airflow.exceptions import AirflowException

from urllib.parse import urljoin

import requests
import time
from requests import exceptions as requests_exceptions

API_HOST = "https://api.spotinst.io/ocean/spark/"
FE_HOST = "https://console.spotinst.com/ocean/spark/"


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

    def _do_api_call(
        self, method: Callable, endpoint: str, payload: Dict = None
    ) -> Dict:
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
            except requests_exceptions.RequestException as e:
                if not _retryable_error(e):
                    # In this case, the user probably made a mistake.
                    # Don't retry.
                    raise AirflowException(
                        "Response: {0}, Status Code: {1}".format(
                            e.response.content, e.response.status_code
                        )
                    )

                self._log_request_error(attempt_num, e)

            if attempt_num == self.retry_limit:
                raise AirflowException(
                    (
                        "API requests to Data Mechanics failed {} times. "
                        + "Giving up."
                    ).format(self.retry_limit)
                )

            attempt_num += 1
            time.sleep(self.retry_delay.total_seconds())

    def _log_request_error(
        self, attempt_num: int, error: requests_exceptions.RequestException
    ) -> None:
        self.log.error(
            "Attempt %s API Request to Data Mechanics failed with reason: %s",
            attempt_num,
            error,
        )

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
        )

    def get_app_page_url(self, app_id: str) -> str:
        return urljoin(
            FE_HOST,
            f"apps/clusters/{self.cluster_id}/apps/{app_id}/overview&accountId={self.account_id}",
        )

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


def _retryable_error(exception: requests_exceptions.RequestException) -> bool:
    return isinstance(
        exception, (requests_exceptions.ConnectionError, requests_exceptions.Timeout)
    ) or (exception.response is not None and exception.response.status_code >= 500)
