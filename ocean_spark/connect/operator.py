from ocean_spark.extra_links import OceanSparkApplicationOverviewLink

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from airflow.models import BaseOperator
from airflow.utils.context import Context
from ocean_spark.connect.hook import (
    DEFAULT_CONN_NAME,
    OceanSparkConnectHook,
)

XCOM_APP_ID_KEY = "app_id"
XCOM_APP_PAGE_URL_KEY = "app_page_url"


class OceanSparkConnectOperator(BaseOperator):
    """
    Submits a Spark Connect task to a Ocean Spark Application through websocket proxy.
    """

    # Used in airflow.models.BaseOperator
    template_fields = (
        "app_id",
        "sql",
        "job_id",
    )
    template_ext = (".json",)
    # "Wave" icon color TODO(crezvoy): check with JY, emily
    ui_color = "#1CB1C2"
    ui_fgcolor = "#fff"
    operator_extra_links = (OceanSparkApplicationOverviewLink(),)

    def __init__(
        self,
        job_id: str = "",
        sql: str = "{{ params.sql }}",
        conn_id: str = DEFAULT_CONN_NAME,
        do_xcom_push: bool = True,
        on_spark_submit_callback: Optional[
            Callable[[OceanSparkConnectHook, str, Context], None]
        ] = None,
        **kwargs: Any,
    ):
        """
        Creates a new ``OceanSparkConnectOperator``.
        """
        super().__init__(**kwargs)

        self.conn_id = conn_id
        self.sql = sql
        self.job_id: Optional[str] = job_id
        self.do_xcom_push: bool = do_xcom_push
        self.on_spark_submit_callback: Optional[
            Callable[[OceanSparkConnectHook, str, Context], None]
        ] = on_spark_submit_callback
        self.hook = self._get_hook()
        if self.job_id is None:
            self.log.info(
                "Setting job name to task id because `job_id` argument is not specified"
            )
            self.job_id = kwargs["task_id"]

    def _get_hook(self) -> OceanSparkConnectHook:
        return OceanSparkConnectHook(
            self.conn_id,
            sql=self.sql,
        )

    def execute(self, context: Context) -> None:
        self.hook.execute(self.sql)
        if self.on_spark_submit_callback:
            try:
                self.on_spark_submit_callback(self.hook, self.hook.app_id, context)
            except Exception as err:
                self.log.exception(err)

    def on_kill(self) -> None:
        self.hook.kill_task()
        self.log.info(
            "Task: %s with app name: %s was requested to be cancelled.",
            self.task_id,
            self.hook.app_id,
        )

    def get_application_overview_url(self) -> str:
        if self.hook.app_id is not None:
            return self._get_hook().get_app_page_url()
        return ""
