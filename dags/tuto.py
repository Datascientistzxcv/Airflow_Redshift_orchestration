from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import psycopg2
import logging

def print_hello(**kwargs):
    hook = PostgresHook(postgres_conn_id="Redshift_youtube")
    conn = hook.get_conn()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(str(kwargs['dag_run'].conf.get('name')))
    result=cursor.fetchall()
    for i in result[:100]:
    #print(result[1]["timestamp"])
        logging.info("################"+kwargs['dag_run'].conf.get('name'))
        f = open('/home/ubuntu/first_odd.txt','a')
        f.write(str(kwargs['dag_run'].conf.get('name')))
        f.close()


dag = DAG('hello_world', description='Simple tutorial DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag,provide_context=True)

dummy_operator >> hello_operator
