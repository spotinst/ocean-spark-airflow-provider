from ocean_spark.hooks import OceanSparkHook


def test_get_driver_logs(
    successful_logs_download: None, get_connection_mock: None
) -> None:
    hook = OceanSparkHook()
    logs = hook.get_driver_logs("test-app-name")
    assert logs[-21:] == "Shutdown hook called\n"
