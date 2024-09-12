import pytest
from unittest.mock import MagicMock
from ocean_spark.operators import OceanSparkOperator
from airflow.exceptions import AirflowException


def test_on_execute(
    successful_submission: None,
    get_app_completed: None,
    get_connection_mock: None,
) -> None:
    operator = OceanSparkOperator(
        job_id="test-job", task_id="test-task", do_xcom_push=False
    )
    operator.execute(context={})


def test_on_execute_failure(
    successful_submission: None,
    get_app_failed: None,
    get_connection_mock: None,
) -> None:
    operator = OceanSparkOperator(
        job_id="test-job",
        task_id="test-task",
        do_xcom_push=False,
        forward_driver_logs=False,
    )
    with pytest.raises(AirflowException):
        operator.execute(context={})


def test_on_execute_failure_forward_logs(
    successful_submission: None,
    get_app_failed: None,
    successful_logs_download: None,
    get_connection_mock: None,
) -> None:
    operator = OceanSparkOperator(
        job_id="test-job",
        task_id="test-task",
        do_xcom_push=False,
        forward_driver_logs=True,
    )
    with pytest.raises(AirflowException):
        operator.execute(context={})
