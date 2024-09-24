from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime, timedelta 

# Define params for Submit Run Operator
notebook_task = {
    'notebook_path': '/workspace/Users/lukedcourcy14@gmail.com/main.py',  # Update this to your actual notebook path in Databricks
}

# Define params for Run Now Operator (if used)
notebook_params = {
    "Variable": 5  # Update this as necessary for your notebook
}

default_args = {
    'owner': '1226d593b7e7',  # Your user ID
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(seconds=120)
}

with DAG(
    '1226d593b7e7_dag',  # Make sure the DAG name is unique
    start_date=datetime(2023, 12, 30),
    schedule_interval='@daily',  # Schedule the DAG to run daily
    catchup=False,
    default_args=default_args
) as dag:

    opr_submit_run = DatabricksSubmitRunOperator(
        task_id='submit_run',
        databricks_conn_id='1226d593b7e7-connector',  # Your Databricks connection name
        existing_cluster_id='1108-162752-8okw8dgg',  # Your existing Databricks cluster ID
        notebook_task=notebook_task  # Pass the notebook task details
    )

    opr_submit_run
