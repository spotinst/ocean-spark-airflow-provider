from datetime import datetime
from typing import cast
from airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from airflow.models.xcom import XCom
from airflow.plugins_manager import AirflowPlugin


class OceanSparkApplicationOverviewLink(BaseOperatorLink):
    name = "Application Overview"

    def get_link(self, operator: BaseOperator, dttm: datetime) -> str:
        url = XCom.get_one(
            execution_date=dttm,
            task_id=operator.task_id,
            key="app_page_url",
        )
        return url
