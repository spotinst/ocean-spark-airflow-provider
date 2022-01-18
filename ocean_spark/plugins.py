from typing import List

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


class OceanSparkPlugin(AirflowPlugin):
    name: str = plugin_name
    operators: List = [OceanSparkOperator]
    hooks: List = [OceanSparkHook]
    executors: List = []
    macros: List = []
    admin_views: List = []
    flask_blueprints: List[Blueprint] = [bp]
    menu_links: List = []
