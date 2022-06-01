"""
# iwb_elektroauto_ladestationen
This DAG updates the following datasets:

- [100196](https://data.bs.ch/explore/dataset/100196)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the iwb_elektroauto_ladestationen docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 6, 1),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('iwb_elektroauto_ladestationen', default_args=default_args, schedule_interval="25 3 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='iwb_elektroauto_ladestationen:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m iwb_elektroauto_ladestationen.etl',
        container_name='iwb_elektroauto_ladestationen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

