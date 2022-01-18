from ocean_spark.hooks import OceanSparkHook
from unittest.mock import MagicMock


def test_kill_app(successful_kill: None, get_connection_mock: None) -> None:
    hook = OceanSparkHook()
    hook.kill_app("delete-app-id")
