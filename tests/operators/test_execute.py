from unittest.mock import MagicMock
from ocean_spark.operators import OceanSparkOperator


def test_on_execute(
    successful_submission: None,
    get_app_completed: None,
    get_connection_mock: None,
) -> None:
    operator = OceanSparkOperator(job_name="test-job", task_id="test-task")
    operator.execute(context={})
