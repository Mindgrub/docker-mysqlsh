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

### Copy Schema Script

We bundled a script to execute [the Copy Schema utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utils-copy.html): `/usr/bin/mysqlsh-copy-schema`

```bash
docker run -i mindgrub/mysqlsh:8.4 /usr/bin/mysqlsh-copy-schema
```

You can use this command along with certain environment variables.

- `SOURCE_HOST`: hostname of source database server
- `SOURCE_PORT`: TCP port for source database server (default: 3306)
- `SOURCE_USER`: username for source database
- `SOURCE_PASSWORD`: password for source database
- `DESTINATION_HOST`: hostname of destination database server
- `DESTINATION_PORT`: TCP port for destination database server (default: 3306)
- `DESTINATION_USER`: username for destination database
- `DESTINATION_PASSWORD`: password for destination database
- `MYSQLSH_THREADS`: number of threads to use for copying (default: 4)
- `MYSQLSH_SSL_MODE`: the MySQL SSL Mode (default: PREFERRED)
- `RECREATE_SCHEMA`: if specified, drop and re-create the existing schema

When the command executes, the `compatibility` argument of the copy schema utility is set to `["strip_definers"]`, and the `consistency` argument is set to `False`.
