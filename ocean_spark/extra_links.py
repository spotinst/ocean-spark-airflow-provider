from datetime import datetime
from typing import cast
from airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from airflow.models.xcom import XCom

import pendulum

APP_PAGE_URL_KEY: str = "app_page_url"


class OceanSparkApplicationOverviewLink(BaseOperatorLink):
    name: str = "Application Overview"

    def get_link(self, operator: BaseOperator, dttm: datetime) -> str:
        url = XCom.get_one(
            execution_date=pendulum.instance(dttm),
            task_id=operator.task_id,
            key=APP_PAGE_URL_KEY,
        )
        if url is None:
            return ""
        return cast(str, url)
