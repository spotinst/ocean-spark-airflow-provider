from airflow.exceptions import AirflowException
import pytest

from ocean_spark.hooks import OceanSparkHook


def test_submit_app(successful_submission: None, get_connection_mock: None) -> None:
    hook = OceanSparkHook()
    app_id = hook.submit_app(payload={})
    assert app_id is not None
    assert app_id == "new-app-id"


def test_failed_submission(failed_submission: None, get_connection_mock: None) -> None:
    hook = OceanSparkHook()
    with pytest.raises(AirflowException):
        hook.submit_app(payload={})
