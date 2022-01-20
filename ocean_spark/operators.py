from datetime import timedelta
import json
from ocean_spark.extra_links import OceanSparkApplicationOverviewLink
import time

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Union

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from ocean_spark.hooks import (
    DEFAULT_CONN_NAME,
    OceanSparkHook,
)
from ocean_spark.application_state import ApplicationState


XCOM_APP_NAME_KEY = "app_name"
XCOM_APP_PAGE_URL_KEY = "app_page_url"


if TYPE_CHECKING:
    from airflow.utils.context import Context


class OceanSparkOperator(BaseOperator):
    """
    Submits a Spark app to Data Mechanics using the `POST /api/apps` API endpoint.
    """

    # Used in airflow.models.BaseOperator
    template_fields = (
        "app_name",
        "job_name",
        "config_template_name",
        "config_overrides",
    )
    template_ext = (".json",)
    # "Wave" icon color TODO(crezvoy): check with JY, emily
    ui_color = "#1CB1C2"
    ui_fgcolor = "#fff"
    operator_extra_links = (OceanSparkApplicationOverviewLink(),)

    @apply_defaults
    def __init__(
        self,
        job_name: str = None,
        app_name: Optional[str] = None,
        config_template_name: Optional[str] = None,
        config_overrides: Optional[Union[Dict, str]] = None,
        conn_id: str = DEFAULT_CONN_NAME,
        polling_period_seconds: int = 10,
        retry_limit: int = 3,
        retry_delay: int = 1,
        do_xcom_push: bool = True,
        on_spark_submit_callback: Optional[
            Callable[[OceanSparkHook, str, Dict], None]
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
        self.retry_delay = timedelta(seconds=retry_delay)
        self.app_name: Optional[str] = None  # will be set from the API response
        self._payload_app_name: Optional[str] = app_name
        self.job_name: Optional[str] = job_name
        self.config_template_name: Optional[str] = config_template_name
        self.config_overrides: Optional[Union[Dict, str]] = config_overrides
        self.do_xcom_push: bool = do_xcom_push
        self.on_spark_submit_callback: Optional[
            Callable[[OceanSparkHook, str, Dict], None]
        ] = on_spark_submit_callback
        self.payload: Dict = {}

        if self.job_name is None:
            self.log.info(
                "Setting job name to task id because `job_name` argument is not specified"
            )
            self.job_name = kwargs["task_id"]

    def _get_hook(self) -> OceanSparkHook:
        return OceanSparkHook(
            self.conn_id,
            retry_limit=self.retry_limit,
            retry_delay=self.retry_delay,
        )

    def _build_payload(self) -> None:
        self.payload["jobId"] = self.job_name
        if self._payload_app_name is not None:
            self.payload["appId"] = self._payload_app_name
        if self.config_template_name is not None:
            self.payload["configTemplateId"] = self.config_template_name

        # templated config overrides dict pulled from xcom is a json str
        if self.config_overrides is not None:
            if isinstance(self.config_overrides, str):
                # json standard requires double quotes
                self.config_overrides = json.loads(
                    self.config_overrides.replace("'", '"')
                )
            self.payload["configOverrides"] = self.config_overrides

    def execute(self, context: Dict) -> None:
        self._build_payload()
        hook = self._get_hook()
        self.app_name = hook.submit_app(self.payload)
        if self.on_spark_submit_callback:
            try:
                self.on_spark_submit_callback(hook, self.app_name, context)
            except Exception as err:
                self.log.exception(err)
        self._monitor_app(hook, context)

    def on_kill(self) -> None:
        if self.app_name is not None:
            hook = self._get_hook()
            hook.kill_app(self.app_name)
        self.log.info(
            "Task: %s with app name: %s was requested to be cancelled.",
            self.task_id,
            self.app_name,
        )

    def get_application_overview_url(self) -> str:
        if self.app_name is not None:
            return self._get_hook().get_app_page_url(self.app_name)
        return ""

    def _monitor_app(self, hook: OceanSparkHook, context: Dict) -> None:

        if self.app_name is None:
            # app not launched
            return
        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_APP_NAME_KEY, value=self.app_name)
        self.log.info("App submitted with app_name: %s", self.app_name)
        app_page_url = hook.get_app_page_url(self.app_name)
        if self.do_xcom_push:
            context["ti"].xcom_push(key=XCOM_APP_PAGE_URL_KEY, value=app_page_url)

        while True:
            app = hook.get_app(self.app_name)
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
