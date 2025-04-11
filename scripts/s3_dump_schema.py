import boto3
import datetime
import json
import os
import urllib.parse
import sys

sfn_token = os.environ.get("SFN_TASK_TOKEN")
sfn = boto3.client('stepfunctions') if sfn_token else None

if sfn_token:
    sfn.send_task_heartbeat(taskToken=sfn_token)

try:
    source_user = os.environ['SOURCE_USER']
    source_password = urllib.parse.quote(os.environ['SOURCE_PASSWORD'])
    source_host = os.environ['SOURCE_HOST']
    source_port = os.environ.get('SOURCE_PORT', '3306')
    source_schema = os.environ['SOURCE_SCHEMA']
    bucket_name = os.environ['BUCKET_NAME']
    bucket_prefix = os.environ.get('BUCKET_PREFIX', 'snapshot-' + datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))
    cli_threads = os.environ.get('MYSQLSH_THREADS', '4')
    cli_ssl_mode = os.environ.get('MYSQLSH_SSL_MODE', 'PREFERRED')

    source_uri = f"{source_user}:{source_password}@{source_host}:{source_port}?ssl-mode={cli_ssl_mode}"
    shell.connect(source_uri)

    if not os.environ.get('AWS_ACCESS_KEY_ID'):
        # MySQL Shell does not use EC2 instance metadata or ECS metadata.
        c = boto3.Session().get_credentials().get_frozen_credentials()._asdict()
        os.environ['AWS_ACCESS_KEY_ID'] = c["access_key"]
        os.environ['AWS_SECRET_ACCESS_KEY'] = c["secret_key"]
        os.environ['AWS_SESSION_TOKEN'] = c["token"]

    util.dump_schemas([source_schema], bucket_prefix, {
        "s3BucketName": bucket_name,
        "threads": cli_threads,
        "showProgress": False,
        "compatibility": ["strip_definers"],
        "consistent": False,
    })

    if sfn_token:
        sfn.send_task_success(
            taskToken=sfn_token,
            output=json.dumps(
                {"bucket": bucket_name, "prefix": bucket_prefix},
                separators=(',', ':'),
            ),
        )

except Exception as e:
    print(e)
    if sfn_token:
        sfn.send_task_failure(
            taskToken=sfn_token,
            error=type(e).__name__,
            cause=f'{e}',
        )
    sys.exit(1)
