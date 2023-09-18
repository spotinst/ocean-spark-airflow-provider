from airflow import DAG, utils
from ocean_spark.operators import (
    OceanSparkOperator,
)

args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "depends_on_past": False,
    "start_date": utils.dates.days_ago(0, second=1),
}


dag = DAG(dag_id="full-example", default_args=args, schedule_interval=None)

parallel_0_task = OceanSparkOperator(
    task_id="parallel-0",
    dag=dag,
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.2.0",
        "image": "gcr.io/datamechanics/spark:platform-3.2-latest",
        "imagePullPolicy": "IfNotPresent",
        "mainClass": "org.apache.spark.examples.SparkPi",
        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",
        "arguments": ["10000"],
        "driver": {
            "cores": 1,
        },
        "executor": {
            "cores": 1,
        },
    },
)

parallel_1_task = OceanSparkOperator(
    task_id="parallel-1",
    dag=dag,
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.2.0",
        "image": "gcr.io/datamechanics/spark:platform-3.2-latest",
        "imagePullPolicy": "IfNotPresent",
        "mainClass": "org.apache.spark.examples.SparkPi",
        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",
        "arguments": ["10000"],
        "driver": {
            "cores": 1,
        },
        "executor": {
            "cores": 1,
        },
    },
)

spark_pi_task = OceanSparkOperator(
    task_id="spark-pi",
    dag=dag,
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.2.0",
        "image": "gcr.io/datamechanics/spark:platform-3.2-latest",
        "imagePullPolicy": "IfNotPresent",
        "mainClass": "org.apache.spark.examples.SparkPi",
        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",
        "arguments": ["10000"],
        "driver": {
            "cores": 1,
        },
        "executor": {
            "cores": 1,
        },
    },
)

failed_app_task = OceanSparkOperator(
    task_id="failed-app",
    dag=dag,
    config_overrides={
        "type": "Scala",
        "mainApplicationFile": "local:///opt/spark/FOO/examples/jars/examples.jar",  # This path does not exist
        "mainClass": "org.apache.spark.examples.SparkPi",
        "arguments": ["10000"],
    },
)

failed_submission_task = OceanSparkOperator(
    task_id="failed-submission",
    dag=dag,
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.2.0",
        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",
        "mainClass": "org.apache.spark.examples.SparkPi",
        "arguments": ["10000"],
        "foo": "bar",  # This field does not exist
    },
)

spark_pi_task.set_upstream([parallel_0_task, parallel_1_task])
failed_app_task.set_upstream(spark_pi_task)
failed_submission_task.set_upstream(spark_pi_task)
