import boto3
import json
import os
import urllib.parse
import sys

sfn_token = os.environ.get("SFN_TASK_TOKEN")
sfn = boto3.client('stepfunctions') if sfn_token else None

if sfn_token:
    sfn.send_task_heartbeat(taskToken=sfn_token)

try:
    dest_user = os.environ['DESTINATION_USER']
    dest_password = urllib.parse.quote(os.environ['DESTINATION_PASSWORD'])
    dest_host = os.environ['DESTINATION_HOST']
    dest_port = os.environ.get('DESTINATION_PORT', '3306')
    dest_schema = os.environ['DESTINATION_SCHEMA']
    bucket_name = os.environ['BUCKET_NAME']
    bucket_prefix = os.environ['BUCKET_PREFIX']
    recreate_schema = os.environ.get('RECREATE_SCHEMA')
    cli_threads = os.environ.get('MYSQLSH_THREADS', '4')
    cli_ssl_mode = os.environ.get('MYSQLSH_SSL_MODE', 'PREFERRED')

    dest_uri = f"{dest_user}:{dest_password}@{dest_host}:{dest_port}?ssl-mode={cli_ssl_mode}"
    shell.connect(dest_uri)

    if recreate_schema:
        print(f"Checking the existence of destination schema: {dest_schema}")
        results = session.run_sql(
            "SELECT default_character_set_name, default_collation_name FROM information_schema.SCHEMATA WHERE schema_name = ?",
            [dest_schema],
        )
        row = results.fetch_one()
        if row:
            print(f"Dropping and re-creating destination schema: {dest_schema}")
            session.run_sql(f"DROP DATABASE {dest_schema}")
            session.run_sql(f"CREATE DATABASE {dest_schema} CHARACTER SET {row[0]} COLLATE {row[1]}")

    if not os.environ.get('AWS_ACCESS_KEY_ID'):
        # MySQL Shell does not use EC2 instance metadata or ECS metadata.
        c = boto3.Session().get_credentials().get_frozen_credentials()._asdict()
        os.environ['AWS_ACCESS_KEY_ID'] = c["access_key"]
        os.environ['AWS_SECRET_ACCESS_KEY'] = c["secret_key"]
        os.environ['AWS_SESSION_TOKEN'] = c["token"]

    util.load_dump(bucket_prefix, {
        "schema": dest_schema,
        "s3BucketName": bucket_name,
        "threads": cli_threads,
        "showProgress": False,
        "progressFile": f"/tmp/load-progress-{bucket_prefix}.json",
    })

    if sfn_token:
        sfn.send_task_success(
            taskToken=sfn_token,
            output=json.dumps(
                {"host": dest_host, "schema": dest_schema},
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
