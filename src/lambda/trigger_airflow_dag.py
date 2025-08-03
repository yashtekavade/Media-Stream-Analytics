import json
import boto3
import urllib3
from datetime import datetime

MWAA_ENV_NAME = "tbsm-MyAirflowEnvironment"
DAG_NAME = "trigger_upsert_glue_job"

def lambda_handler(event, context):
    print("📦 Received S3 Event:")
    print(json.dumps(event, indent=2))

    mwaa = boto3.client('mwaa')

    try:
        # 1. Create MWAA CLI token
        resp = mwaa.create_cli_token(Name=MWAA_ENV_NAME)
        web_token = resp['CliToken']
        web_server_hostname = resp['WebServerHostname']
        print("🔐 CLI token and hostname retrieved successfully.")

        # 2. Generate Airflow CLI trigger command
        execution_date = datetime.utcnow().isoformat()
        cli_command = f"dags trigger -e {execution_date} {DAG_NAME}"
        trigger_url = f"https://{web_server_hostname}/aws_mwaa/cli"

        print(f"🚀 Triggering DAG: {DAG_NAME} at {execution_date}")

        # 3. Send request using urllib3
        http = urllib3.PoolManager()
        headers = {
            "Authorization": f"Bearer {web_token}",
            "Content-Type": "text/plain"
        }

        response = http.request(
            "POST",
            trigger_url,
            headers=headers,
            body=cli_command.encode("utf-8"),
            timeout=10.0
        )

        # 4. Handle response
        status = response.status
        response_body = response.data.decode("utf-8")

        print(f"🌐 HTTP Status: {status}")
        print(f"🧾 Response Body:\n{response_body}")

        return {
            'statusCode': status,
            'body': json.dumps({
                'message': f"DAG trigger attempted with status {status}",
                'response': response_body
            })
        }

    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
