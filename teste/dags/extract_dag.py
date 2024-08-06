from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from helpers.postgres_helper import check_table_exists, extract_data
from helpers.file_helper import copy_to_current_data

def check_table():
    check_table_exists('sales')

def extract():
    today_date = datetime.today().strftime('%Y%m%d')
    output_path = f"/opt/airflow/data/{today_date}/Amazon_data.csv"
    extract_data('SELECT * FROM sales', output_path)

def copy_data():
    today_date = datetime.today().strftime('%Y%m%d')
    source_path = f"/opt/airflow/data/{today_date}/Amazon_data.csv"
    dest_path = "/opt/airflow/data/current_data/Amazon_data.csv"
    copy_to_current_data(source_path, dest_path)

# Default args for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 1),
    'retries': 1,
}

# Define the DAG
with DAG('amazon_data_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    check_table_task = PythonOperator(
        task_id='check_table_exists',
        python_callable=check_table
    )

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract
    )

    copy_data_task = PythonOperator(
        task_id='copy_to_current_data',
        python_callable=copy_data
    )

    check_table_task >> extract_task >> copy_data_task
