from ocean_spark.hooks import OceanSparkHook
from unittest.mock import MagicMock


def test_get_app(successful_get_app: None, get_connection_mock: None) -> None:
    hook = OceanSparkHook()
    app_dict = hook.get_app("test-app-name")
    assert app_dict is not None
    assert app_dict["displayName"] == "test app name"
