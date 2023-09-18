from airflow import DAG, utils
from ocean_spark.operators import (
    OceanSparkOperator,
)

args = {
    "owner": "airflow",
    "email": [],  # ["airflow@example.com"],
    "depends_on_past": False,
    "start_date": utils.dates.days_ago(0, second=1),
}


dag = DAG(dag_id="failed-app", default_args=args, schedule_interval=None)

word_count_task = OceanSparkOperator(
    task_id="failed-word-count",
    dag=dag,
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.2.0",
        "mainApplicationFile": "local:///opt/spark/examples/FOO/jars/examples.jar",  # This path does not exist
        "mainClass": "org.apache.spark.examples.SparkPi",
        "arguments": ["10000"],
    },
)
