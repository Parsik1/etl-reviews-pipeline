from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from etl.extract import extract_reviews
from etl.transform import transform_reviews
from etl.load import load_to_sqlite


with DAG(
    dag_id="reviews_etl_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["coursework"],
) as dag:
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_reviews,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_reviews,
        op_args=[extract_task.output],
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_to_sqlite,
        op_args=[transform_task.output],
    )

    extract_task >> transform_task >> load_task
