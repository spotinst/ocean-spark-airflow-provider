FROM puckel/docker-airflow:1.10.9

COPY  --chown=airflow:airflow ./dist ./dist
RUN pip install ./dist/*.whl
