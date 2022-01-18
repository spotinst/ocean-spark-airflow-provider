from apache/airflow:2.2.3-python3.7

COPY  --chown=airflow:airflow ./dist ./dist
RUN pip install ./dist/*.whl
