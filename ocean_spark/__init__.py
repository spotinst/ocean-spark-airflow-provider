from packaging import version
from typing import Dict

from airflow import __version__

import ocean_spark.hooks
import ocean_spark.operators
import ocean_spark.extra_links


def get_provider_info() -> Dict:
    info = {
        "versions": [
            "1.1.0",
            "1.0.0",
            "0.1.3",
            "0.1.2",
            "0.1.1",
            "0.1.0",
        ],
        "package-name": "ocean-spark-airflow-provider",
        "name": "Ocean for Spark Airflow Provider",
        "description": "Apache Airflow connector for Ocean for Apache Spark",
        "hook-class-names": [
            "ocean_spark.hooks.OceanSparkHook",
        ],
        "connection-types": [
            {
                "hook-class-name": "ocean_spark.hooks.OceanSparkHook",
                "connection-type": "ocean_spark",
            }
        ],
        "extra-links": ["ocean_spark.extra_links.OceanSparkApplicationOverviewLink"],
    }

    # Pyspark 3.4.0 (that allow spark Connect) is only available from Airflow 2.6.2
    if version.parse(__version__) >= version.parse("2.6.2"):
        info["hook-class-names"] = [
            "ocean_spark.hooks.OceanSparkHook",
            "ocean_spark.hooks.OceanSparkConnectHook",
        ]

        info["connection-types"] = [
            {
                "hook-class-name": "ocean_spark.hooks.OceanSparkHook",
                "connection-type": "ocean_spark",
            },
            {
                "hook-class-name": "ocean_spark.hooks.OceanSparkConnectHook",
                "connection-type": "ocean_spark_connect",
            },
        ]

    return info
