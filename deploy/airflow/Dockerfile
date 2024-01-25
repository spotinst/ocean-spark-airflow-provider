ARG AIRFLOW_VERSION
ARG AIRFLOW_PYTHON_VERSION

FROM apache/airflow:${AIRFLOW_VERSION}-python${AIRFLOW_PYTHON_VERSION}
ARG AIRFLOW_PYTHON_VERSION

COPY  --chown=airflow:airflow ./dist ./dist
RUN pip install -c https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${AIRFLOW_PYTHON_VERSION}.txt ./dist/*.whl
