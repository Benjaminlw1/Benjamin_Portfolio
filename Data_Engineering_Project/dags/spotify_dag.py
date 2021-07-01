from datetime import datetime, timedelta
import datetime
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from spotify_etl import run_spotify_etl

tdy = datetime.datetime.now()
currentMonth = tdy.month

default_args = {
    'owner' : "airflow",
    'depends_on_past' : False,
    'start_date' : datetime.datetime(2021,7,1),
    'email' : ['benjaminlw1@hotmail.com'],
    'email_on_retry' : True,
    'email_on_failure' : True,
    'retries' : 3,
    'retry_delay' : timedelta(minutes=1),
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Dag with Spotify ETL process',
    schedule_interval='@monthly',
    )

run_etl = PythonOperator(
        task_id = 'spotify_etl',
        python_callable=run_spotify_etl,
        dag=dag

    )

email = EmailOperator(
        task_id='send_email',
        to='benjaminlw1@hotmail.com',
        subject='Airflow Alert spotify etl',
        html_content="""<h3> Email Trigger batch spotify etl for {currentMonth}. Thank you </h3>""",
        dag=dag
    )

run_etl >> email
