"""
# mobilitaet_dtv.py
This DAG updates the following datasets:

- [100199](https://data.bs.ch/explore/dataset/100199)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the mobilitaet_dtv docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 7, 22),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('mobilitaet_dtv', default_args=default_args, schedule_interval="0 3 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='mobilitaet_dtv:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m mobilitaet_dtv.etl',
        container_name='mobilitaet_dtv--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

