from datetime import timedelta
import json
from ocean_spark.extra_links import OceanSparkApplicationOverviewLink
from packaging import version
import time

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union

from airflow import __version__
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator

from ocean_spark.hooks import (
    DEFAULT_CONN_NAME,
    OceanSparkHook,
)
from ocean_spark.application_state import ApplicationState

if TYPE_CHECKING:
    from airflow.utils.context import Context

XCOM_APP_ID_KEY = "app_id"
XCOM_APP_PAGE_URL_KEY = "app_page_url"

# Pyspark 3.4.0 (that allow spark Connect) is only available from Airflow 2.6.2
if version.parse(__version__) >= version.parse("2.6.2"):
    from ocean_spark.connect.operator import OceanSparkConnectOperator  # noqa: F401


class OceanSparkOperator(BaseOperator):
    """
    Submits a Spark app to Data Mechanics using the `POST /api/apps` API endpoint.
    """

    # Used in airflow.models.BaseOperator
    template_fields = (
        "app_id",
        "job_id",
        "config_template_id",
        "config_overrides",
    )
    template_ext = (".json",)
    # "Wave" icon color TODO(crezvoy): check with JY, emily
    ui_color = "#1CB1C2"
    ui_fgcolor = "#fff"
    operator_extra_links = (OceanSparkApplicationOverviewLink(),)

    def __init__(
        self,
        job_id: str = "",
        app_id: Optional[str] = None,
        config_template_id: Optional[str] = None,
        config_overrides: Optional[Union[Dict, str]] = None,
        conn_id: str = DEFAULT_CONN_NAME,
        polling_period_seconds: int = 10,
        retry_limit: int = 3,
        retry_delay: Union[timedelta, int] = timedelta(seconds=1),
        do_xcom_push: bool = True,
        on_spark_submit_callback: Optional[
            Callable[[OceanSparkHook, str, "Context"], None]
        ] = None,
        **kwargs: Any,
    ):
        """
        Creates a new ``OceanSparkOperator``.
        """
        super().__init__(**kwargs)

        self.conn_id = conn_id
        self.polling_period_seconds = polling_period_seconds
        self.retry_limit = retry_limit
        self.retry_delay = (
            retry_delay
            if isinstance(retry_delay, timedelta)
            else timedelta(seconds=retry_delay)
        )
        self.app_id: Optional[str] = None  # will be set from the API response
        self._payload_app_id: Optional[str] = app_id
        self.job_id: Optional[str] = job_id
        self.config_template_id: Optional[str] = config_template_id
        self.config_overrides: Optional[Union[Dict, str]] = config_overrides
        self.do_xcom_push: bool = do_xcom_push
        self.on_spark_submit_callback: Optional[
            Callable[[OceanSparkHook, str, "Context"], None]
        ] = on_spark_submit_callback
        self.payload: Dict = {}

        if self.job_id is None:
            self.log.info(
                "Setting job name to task id because `job_id` argument is not specified"
            )
            self.job_id = kwargs["task_id"]

    def _get_hook(self) -> OceanSparkHook:
        return OceanSparkHook(
            self.conn_id,
            retry_limit=self.retry_limit,
            retry_delay=self.retry_delay,
        )

    def _build_payload(self) -> None:
        self.payload["jobId"] = self.job_id
        if self._payload_app_id is not None:
            self.payload["appId"] = self._payload_app_id
        if self.config_template_id is not None:
            self.payload["configTemplateId"] = self.config_template_id

        # templated config overrides dict pulled from xcom is a json str
        if self.config_overrides is not None:
            if isinstance(self.config_overrides, str):
                try:
                    self.config_overrides = json.loads(self.config_overrides)
                except json.JSONDecodeError as e:
                    raise AirflowException(
                        f"Failed to parse config_overrides as JSON: {e}"
                    )

            self.payload["configOverrides"] = self.config_overrides

    def execute(self, context: "Context") -> None:
        self._build_payload()
        hook = self._get_hook()
        self.app_id = hook.submit_app(self.payload)
        if self.on_spark_submit_callback:
            try:
                self.on_spark_submit_callback(hook, self.app_id, context)
            except Exception as err:
                self.log.exception(err)
        self._monitor_app(hook, context)

    def on_kill(self) -> None:
        if self.app_id is not None:
            hook = self._get_hook()
            hook.kill_app(self.app_id)
        self.log.info(
            "Task: %s with app name: %s was requested to be cancelled.",
            self.task_id,
            self.app_id,
        )

    def get_application_overview_url(self) -> str:
        if self.app_id is not None:
            return self._get_hook().get_app_page_url(self.app_id)
        return ""

    def _monitor_app(self, hook: OceanSparkHook, context: "Context") -> None:
        if self.app_id is None:
            # app not launched
            return
        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_APP_ID_KEY, value=self.app_id)
        self.log.info("App submitted with app_id: %s", self.app_id)
        app_page_url = hook.get_app_page_url(self.app_id)
        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_APP_PAGE_URL_KEY, value=app_page_url)

        while True:
            app = hook.get_app(self.app_id)
            app_state = _get_state_from_app(app)
            self.log.info("View app details at %s", app_page_url)
            if app_state.is_terminal:
                if app_state.is_successful:
                    self.log.info("%s completed successfully.", self.task_id)
                    return
                else:
                    error_message = "{t} failed with terminal state: {s}".format(
                        t=self.task_id, s=app_state.value
                    )
                    raise AirflowException(error_message)
            else:
                self.log.info("%s in app state: %s", self.task_id, app_state.value)
                self.log.info("Sleeping for %s seconds.", self.polling_period_seconds)
                time.sleep(self.polling_period_seconds)


def _get_state_from_app(app: Dict) -> ApplicationState:
    return ApplicationState(app.get("appState", "PENDING"))
