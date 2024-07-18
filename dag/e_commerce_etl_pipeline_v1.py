from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 18),
    'email_on_failure': True, #send email notifications on task failures 
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG object
dag = DAG(
    'E-commerce_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for E-commerce data',
    schedule_interval='0 */3 * * *',  # Runs every 3 hours
    catchup=False,
)

# Define tasks using PythonOperator to run Python scripts
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable='python /path/extract_data_v1.py',  # Path to your extract script
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable='python /path/transform_data_v1.py',  # Path to your transform script
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable='python /path/load_data_v1.py',  # Path to your load script
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
