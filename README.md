# docker-mysqlsh

[![Docker Pulls](https://img.shields.io/docker/pulls/mindgrub/mysqlsh?logo=docker&logoColor=white)](https://hub.docker.com/r/mindgrub/mysqlsh) [![Release Status](https://github.com/Mindgrub/docker-mysqlsh/actions/workflows/release.yml/badge.svg)](https://github.com/Mindgrub/docker-mysqlsh/actions/workflows/release.yml)

A Docker image for the community release of [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/).

## Versions and Tags Available

- [8.4.x: `latest`, `8`, `8.4`, `8.4-debian`, `8.4-bookworm`](8.4/Dockerfile)
  - Tags also exist for the full version numbers (e.g. `8.4.4-debian`, `8.4.4-bookworm`)
- [8.0.x: `8.0`, `8.0-debian`, `8.0-bookworm`](8.0/Dockerfile)
  - Tags also exist for the full version numbers (e.g. `8.0.41-debian`, `8.0.41-bookworm`)

### CPU Architecture

Because Oracle only provides an [APT repository for x86_64 binaries](https://repo.mysql.com/apt/), this image is only available on the `linux/amd64` architecture.

## Usage

```bash
# Run the interactive MySQL Shell prompt
docker run -it mindgrub/mysqlsh:8.4
```

### Dump Schema to S3

We bundled a Python script to execute [the Schema Dump utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.html) and export to Amazon S3: `/s3_dump_schema.py`

```bash
docker run mindgrub/mysqlsh:8.4 mysqlsh --py -f s3_dump_schema.py
```

You can use this command along with certain environment variables.

- `SOURCE_HOST`: hostname of source database server
- `SOURCE_PORT`: TCP port for source database server (default: 3306)
- `SOURCE_USER`: username for source database
- `SOURCE_PASSWORD`: password for source database
- `SOURCE_SCHEMA` – the name of the database to dump
- `BUCKET_NAME`: the name of the AWS S3 bucket
- `BUCKET_PREFIX`: the directory prefix to use for the AWS S3 objects (default: snapshot-xxxxxxxxTxxxxxx using ISO date/time)
- `MYSQLSH_THREADS`: number of threads to use for dumping (default: 4)
- `MYSQLSH_SSL_MODE`: the MySQL SSL Mode (default: PREFERRED)
- `SFN_TASK_TOKEN` – Optional. A Step Functions [Task Token](https://docs.aws.amazon.com/step-functions/latest/apireference/API_GetActivityTask.html#StepFunctions-GetActivityTask-response-taskToken). If present, this token will be used to call [`SendTaskHeartbeat`](https://docs.aws.amazon.com/step-functions/latest/apireference/API_SendTaskHeartbeat.html) and [`SendTaskSuccess`](https://docs.aws.amazon.com/step-functions/latest/apireference/API_SendTaskSuccess.html). The task output sent to `SendTaskSuccess` will consist of a JSON object with two properties: `bucket` and `prefix`. Errors will be reported via `SendTaskFailure`.

#### AWS Permissions

If this Docker image is used within Amazon ECS, specify permissions to S3 (and optionally Step Functions) within your Task Definition role. Otherwise, you can provide `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as environment variables.

### Load Schema from S3

We bundled a Python script to execute [the Dump Load utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-load-dump.html) from an export stored in Amazon S3: `/s3_load_schema.py`

```bash
docker run mindgrub/mysqlsh:8.4 mysqlsh --py -f s3_load_schema.py
```

You can use this command along with certain environment variables.

- `DESTINATION_HOST`: hostname of destination database server
- `DESTINATION_PORT`: TCP port for destination database server (default: 3306)
- `DESTINATION_USER`: username for destination database
- `DESTINATION_PASSWORD`: password for destination database
- `DESTINATION_SCHEMA` – the name of the database to restore into
- `BUCKET_NAME`: the name of the AWS S3 bucket
- `BUCKET_PREFIX`: the S3 prefix of the dump directory
- `RECREATE_SCHEMA`: if specified, drop and re-create the existing schema
- `MYSQLSH_THREADS`: number of threads to use for loading (default: 4)
- `MYSQLSH_SSL_MODE`: the MySQL SSL Mode (default: PREFERRED)
- `SFN_TASK_TOKEN` – Optional. A Step Functions [Task Token](https://docs.aws.amazon.com/step-functions/latest/apireference/API_GetActivityTask.html#StepFunctions-GetActivityTask-response-taskToken). If present, this token will be used to call [`SendTaskHeartbeat`](https://docs.aws.amazon.com/step-functions/latest/apireference/API_SendTaskHeartbeat.html) and [`SendTaskSuccess`](https://docs.aws.amazon.com/step-functions/latest/apireference/API_SendTaskSuccess.html). The task output sent to `SendTaskSuccess` will consist of a JSON object with two properties: `host` and `schema`. Errors will be reported via `SendTaskFailure`.

#### AWS Permissions

If this Docker image is used within Amazon ECS, specify permissions to S3 (and optionally Step Functions) within your Task Definition role. Otherwise, you can provide `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as environment variables.

### Copy Schema Script

We bundled a script to execute [the Copy Schema utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utils-copy.html): `/copy_schema.py` (this script is _not_ available in the 8.0 image).

```bash
# New method
docker run -i mindgrub/mysqlsh:8.4 mysqlsh --py -f copy_schema.py
# Deprecated
docker run -i mindgrub/mysqlsh:8.4 /usr/bin/mysqlsh-copy-schema
```

You can use this command along with certain environment variables.

- `SOURCE_HOST`: hostname of source database server
- `SOURCE_PORT`: TCP port for source database server (default: 3306)
- `SOURCE_USER`: username for source database
- `SOURCE_PASSWORD`: password for source database
- `SOURCE_SCHEMA` – the name of the database to dump
- `DESTINATION_HOST`: hostname of destination database server
- `DESTINATION_PORT`: TCP port for destination database server (default: 3306)
- `DESTINATION_USER`: username for destination database
- `DESTINATION_PASSWORD`: password for destination database
- `DESTINATION_SCHEMA` – the name of the database to restore into
- `MYSQLSH_THREADS`: number of threads to use for copying (default: 4)
- `MYSQLSH_SSL_MODE`: the MySQL SSL Mode (default: PREFERRED)
- `RECREATE_SCHEMA`: if specified, drop and re-create the existing schema

When the command executes, the `compatibility` argument of the copy schema utility is set to `["strip_definers"]`, and the `consistency` argument is set to `False`.
