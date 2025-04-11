import datetime
import os
import urllib.parse
import sys

try:
    source_user = os.environ['SOURCE_USER']
    source_password = urllib.parse.quote(os.environ['SOURCE_PASSWORD'])
    source_host = os.environ['SOURCE_HOST']
    source_port = os.environ.get('SOURCE_PORT', '3306')
    source_schema = os.environ['SOURCE_SCHEMA']
    dest_user = os.environ['DESTINATION_USER']
    dest_password = urllib.parse.quote(os.environ['DESTINATION_PASSWORD'])
    dest_host = os.environ['DESTINATION_HOST']
    dest_port = os.environ.get('DESTINATION_PORT', '3306')
    dest_schema = os.environ['DESTINATION_SCHEMA']
    recreate_schema = os.environ.get('RECREATE_SCHEMA')
    cli_threads = os.environ.get('MYSQLSH_THREADS', '4')
    cli_ssl_mode = os.environ.get('MYSQLSH_SSL_MODE', 'PREFERRED')

    dest_uri = f"{dest_user}:{dest_password}@{dest_host}:{dest_port}?ssl-mode={cli_ssl_mode}"

    if recreate_schema:
        print(f"Checking the existence of destination schema: {dest_schema}")
        dest_session = shell.open_session(dest_uri)
        results = dest_session.run_sql(
            "SELECT default_character_set_name, default_collation_name FROM information_schema.SCHEMATA WHERE schema_name = ?",
            [dest_schema],
        )
        row = results.fetch_one()
        if row:
            print(f"Dropping and re-creating destination schema: {dest_schema}")
            dest_session.run_sql(f"DROP DATABASE {dest_schema}")
            dest_session.run_sql(f"CREATE DATABASE {dest_schema} CHARACTER SET {row[0]} COLLATE {row[1]}")
        dest_session.close()

    source_uri = f"{source_user}:{source_password}@{source_host}:{source_port}?ssl-mode={cli_ssl_mode}"
    shell.connect(source_uri)

    util.copy_schemas([source_schema], dest_uri, {
        "schema": dest_schema,
        "threads": cli_threads,
        "showProgress": False,
        "compatibility": ["strip_definers"],
        "consistent": False,
    })

except Exception as e:
    print(e)
    sys.exit(1)
