from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOpera
from datetime import datetime

with DAG(
    dag_id='run_glue_demographics_etl',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['iceberg', 'glue', 'etl']
) as dag:

    run_glue_job = AwsGlueJobOperator (
        task_id='run_iceberg_merge_job',
        job_name='tbsm-ice',
        script_location='s3://aws-glue-assets-008673239246-ap-southeast',
        aws_conn_id='aws_default',
        region_name='ap-southeast-2'
    )
