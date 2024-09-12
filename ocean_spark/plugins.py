from packaging import version
from typing import List, Any

from airflow import __version__
from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint  # type: ignore

from ocean_spark.hooks import OceanSparkHook
from ocean_spark.operators import OceanSparkOperator

plugin_name = "ocean_spark"

bp = Blueprint(
    plugin_name,
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/" + plugin_name,
)


_operatorList: Any = [OceanSparkOperator]
_hookList: Any = [OceanSparkHook]

# Pyspark 3.4.0 (that allow spark Connect) is only available from Airflow 2.6.2
if version.parse(__version__) >= version.parse("2.6.2"):
    from ocean_spark.hooks import OceanSparkConnectHook
    from ocean_spark.operators import OceanSparkConnectOperator

    _operatorList = [OceanSparkOperator, OceanSparkConnectOperator]
    _hookList = [OceanSparkHook, OceanSparkConnectHook]


class OceanSparkPlugin(AirflowPlugin):
    name: str = plugin_name
    operators: List = _operatorList
    hooks: List = _hookList
    executors: List = []
    macros: List = []
    admin_views: List = []
    flask_blueprints: List[Blueprint] = [bp]
    menu_links: List = []
