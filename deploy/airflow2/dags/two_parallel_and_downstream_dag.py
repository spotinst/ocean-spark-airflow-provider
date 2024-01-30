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

dag = DAG(
    dag_id="two-parallel-and-downstream",
    default_args=args,
    schedule_interval=None
)


parallel_0_task = OceanSparkOperator(
    task_id="synthetictestingservice-with-job-id",
    dag=dag,
    conn_id="ocean_spark_mathilde_prod",
    job_id="synthetictestingservice-syntheticroutesu",
    app_display_name="SyntheticTestingService.SyntheticRouteSummary.Copydog3.Raw",
    config_overrides=
        {
        "type": "Scala",
        "sparkVersion": "3.0.0",
        "image": "public.ecr.aws/ocean-spark/spark:platform-3.2.1-latest",
        "mainClass": "org.apache.spark.examples.SparkPi",
        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",
        "arguments": [
            "100"
        ]
}
)


parallel_1_task = OceanSparkOperator(
    task_id="synthetictestingservice-syntheticroutesu",
    dag=dag,
    conn_id="ocean_spark_mathilde_prod",
    app_display_name="SyntheticTestingService.SyntheticRouteSummaryExperiment.Copydog3.Raw",
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.0.0",
        "image": "public.ecr.aws/ocean-spark/spark:platform-3.2.1-latest",
        "mainClass": "DriverNoJob",
        "mainApplicationFile": "s3://bigdata-spark-images-integration-test/code/oom_studies/scala_oom_udf_compute_10g.jar",
        "arguments": [
            "100"
        ]
}
)

downstream = OceanSparkOperator(
    task_id="airflow-demo-downstream",
    dag=dag,
    conn_id="ocean_spark_mathilde_prod",
    config_overrides={
        "type": "Scala",
        "sparkVersion": "3.2.0",
        "image": "gcr.io/datamechanics/spark:platform-3.2-latest",
        "imagePullPolicy": "IfNotPresent",
        "mainClass": "org.apache.spark.examples.SparkPi",
        "mainApplicationFile": "local:///opt/spark/examples/jars/examples.jar",
        "arguments": ["1000"]
    }
)

downstream.set_upstream([parallel_0_task, parallel_1_task])