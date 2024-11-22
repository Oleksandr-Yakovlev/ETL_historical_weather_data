import sys
sys.path.append('/home/tuuli/airflow/dags/Data_Eng_TeamProject')

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from extract_module import extract_data
from transform_module import transform_data
from validate_module import validate_data
from load_module import load_data

default_args = {
    'owner': 'Team-Project_ETL',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# Define the DAG
dag = DAG(
    'Historical_weather_data',
    default_args=default_args,
    description='ETL pipeline for Historical weather data with validation and trigger rules',
    schedule_interval='@daily',
)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

validate_task = PythonOperator(
    task_id='validate_task',
    python_callable=validate_data,
    provide_context=True,
    trigger_rule='all_success',  # Proceed only if all previous tasks succeed
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    provide_context=True,
    trigger_rule='all_success', # Proceed only if validation is successful
    dag=dag,
    )

extract_task >> transform_task >> validate_task >> load_task
