from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the kapo_geschwindigkeitsmonitoring docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2021, 1, 20),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('aue-schall', default_args=default_args, schedule_interval="30 0 * * *", catchup=False) as dag:
        upload = DockerOperator(
                task_id='upload',
                image='kapo_geschwindigkeitsmonitoring:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/kapo_geschwindigkeitsmonitoring/etl.sh ',
                container_name='kapo_geschwindigkeitsmonitoring',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch/KaPo/VP-Geschwindigkeitsmonitoring:/code/data-processing/kapo_geschwindigkeitsmonitoring/data_orig',
                         '/data/dev/workspace/data-processing:/code/data-processing']
        )

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl da_npx2b3,da_b319m2',
                container_name='kapo_geschwindigkeitsmonitoring--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=2,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish