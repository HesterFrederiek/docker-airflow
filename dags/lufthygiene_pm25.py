from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the lufthygiene_pm25 docker container',
    'depend_on_past': False,
    'start_date': datetime(2021, 2, 22),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('lufthygiene_pm25', default_args=default_args, schedule_interval="*/15 * * * *", catchup=False) as dag:
    upload = DockerOperator(
        task_id='upload',
        image='lufthygiene_pm25:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/lufthygiene_pm25/etl.sh ',
        container_name='lufthygiene_pm25',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
