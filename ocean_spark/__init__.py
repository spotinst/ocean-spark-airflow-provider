from typing import Dict
import ocean_spark.hooks
import ocean_spark.operators
import ocean_spark.extra_links
import ocean_spark.connect_hook
import ocean_spark.connect_operator


def get_provider_info() -> Dict:
    return {
        "versions": [
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
            "ocean_spark.connect_hook.OceanSparkConnectHook",
        ],
        "connection-types": [
            {
                "hook-class-name": "ocean_spark.hooks.OceanSparkHook",
                "connection-type": "ocean_spark",
            },
        ],
        "extra-links": ["ocean_spark.extra_links.OceanSparkApplicationOverviewLink"],
    }
