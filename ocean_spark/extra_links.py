from pendulum import DateTime
from typing import cast, TYPE_CHECKING
from airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from airflow.models.xcom import XCom

if TYPE_CHECKING:
    from airflow.models.taskinstancekey import TaskInstanceKey

APP_PAGE_URL_KEY: str = "app_page_url"


class OceanSparkApplicationOverviewLink(BaseOperatorLink):
    name: str = "Application Overview"

    def get_link(self, operator: BaseOperator, *, ti_key: "TaskInstanceKey") -> str:
        if isinstance(operator.start_date, DateTime):
            url = XCom.get_one(
                execution_date=operator.start_date,
                task_id=operator.task_id,
                key=APP_PAGE_URL_KEY,
            )
            if url is not None:
                return cast(str, url)
        return ""
