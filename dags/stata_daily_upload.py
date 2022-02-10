"""
# stata_daily_upload
This DAG updates datasets referenced in https://github.com/opendatabs/data-processing/blob/master/stata_daily_upload/etl.py:
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the stata_daily_upload docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 9, 23),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=30)
}

with DAG('stata_daily_upload', default_args=default_args, schedule_interval="*/5 * * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='stata_daily_upload:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/stata_daily_upload/etl.sh ',
                container_name='stata_daily_upload',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch:/code/data-processing/stata_daily_upload/data', '/data/dev/workspace/data-processing:/code/data-processing']
        )

        # ods_publish = DockerOperator(
        #         task_id='ods-publish',
        #         image='ods-publish:latest',
        #         api_version='auto',
        #         auto_remove=True,
        #         command='python3 -m ods_publish.etl_id 100074,100079,100092,100099,100106,100107,100125,100126,100127,100128,100129',
        #         container_name='stata_daily_upload--ods-publish',
        #         docker_url="unix://var/run/docker.sock",
        #         network_mode="bridge",
        #         tty=True,
        #         volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        #         retry=5,
        #         retry_delay=timedelta(minutes=5)
        # )
        #
        # upload >> ods_publish