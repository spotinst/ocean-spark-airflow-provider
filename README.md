# Airflow connector to Ocean for Apache Spark

An Airflow plugin and provider to launch and monitor Spark
applications on [Ocean for
Apache Spark](https://spot.io/products/ocean-apache-spark/).

## Compatibility

`ocean-spark-airflow-provider` is compatible with both Airflow 1 and
Airflow 2. It is detected as an Airflow plugin by Airflow 1 and up,
and as a provider by Airflow 2.


## Installation

```
pip install ocean-spark-airflow-provider
```

## Usage

For general usage of Ocean for Apache Spark, refer to the [official
documentation](https://docs.spot.io/ocean-spark/getting-started/?id=get-started-with-ocean-for-apache-spark).

### Setting up the connection

In the connection menu, register a new connection of type **Ocean for
Apache Spark**. The default connection name is `ocean_spark_default`. You will
need to have:

 - The Ocean Spark cluster ID of the cluster you just created (of the
   format `osc-e4089a00`). You can find it in the Spot console in the
   [list of
   clusters](https://docs.spot.io/ocean-spark/product-tour/manage-clusters),
   or by using the [Cluster
   List](https://docs.spot.io/api/#operation/OceanSparkClusterList) API.
 - [A Spot
   token](https://docs.spot.io/administration/api/create-api-token?id=create-an-api-token)
   to interact with the Spot API.
 
![connection setup dialog](./images/connection_setup.png) 

The **Ocean for Apache Spark** connection type is not available for Airflow
1, instead create an **HTTP** connection and fill your cluster id as
**host**, and your API token as **password**.

You will need to create a separate connection for each Ocean Spark
cluster that you want to use with Airflow.  In the
`OceanSparkOperator`, you can select which Ocean Spark connection to
use with the `connection_name` argument (defaults to
`ocean_spark_default`). For example, you may choose to have one 
Ocean Spark cluster per environment (dev, staging, prod), and you
can easily target an environment by picking the correct Airflow connection.

### Using the operator

```python
from airflow import __version__ as airflow_version
if airflow_version.starts_with("1."):
    # Airflow 1, import as plugin
    from airflow.operators.ocean_spark import OceanSparkOperator
else:
    # Airflow 2
    from ocean_spark.operators import OceanSparkOperator
    
# DAG creation
    
spark_pi_task = OceanSparkOperator(
    job_id="spark-pi",
    task_id="compute-pi",
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
            "spot": false
        },
        "executor": {
            "cores": 4,
            "instances": 1,
            "spot": true,
            "instanceSelector": "r5"
        },
    },
)
```

more examples are available for [Airflow 1](./deploy/airflow1/example_dags) and [Airflow 2](./deploy/airflow2/dags).

## Test locally

You can test the plugin locally using the docker compose setup in this
repository. Run `make serve_airflow2` at the root of the repository to
launch an instance of Airflow 2 with the provider already installed.
