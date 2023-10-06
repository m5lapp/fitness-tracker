# fitness-tracker
A very simple web application for tracking fitness progress. Developed using Django's admin interface.

## Local Development
For local development, create a .envrc file with the following content and load it with `source .envrc`. Replace any UPPER_CASE_PLACEHOLDERS with appropriate values.

```bash
export CONTAINER_CMD=podman

# Container registry details required for pushing and possibly pulling images.
export CONTAINER_REGISTRY=docker.io
export CONTAINER_REGISTRY_ACCESS_TOKEN='REGISTRY_ACCESS_TOKEN'
export CONTAINER_REGISTRY_USER=REGISTRY_USER_NAME

# Build environment variables.
export NGINX_SERVER_NAME=APP_FQDN

# Application environment variables.
export FT_ALLOWED_HOSTS=127.0.0.1,localhost
export FT_DB_ENGINE=sqlite3
export FT_DB_NAME=app/db.sqlite3
export FT_DB_HOST=DB_HOST_URL
export FT_DB_PORT="5432"
export FT_DB_USERNAME=fitness_tracker_dev_user
export FT_DB_PASSWORD=password

export FT_DEBUG=1

export FT_SECRET_KEY='DJANGO_SECRET_KEY'
```

You can then perform various tasks with the targets in the Makefile such as running a development server, accessing a Django shell, running management commands and creating database migrations. You can see a complete list of the available commands by running `make help`.

## Deployment Steps

1. Create a .envrc file as described in the Local Development section and load it with `source .envrc`
1. Copy all the static files to the proxy directory: `make collectstatic`
1. Log in to the container registry: `make build/login`
1. Build and push the proxy and application container images:
    1. `make build/container/proxy`
    1. `make build/container/app`
1. When the application is running for the first time, you will need to create a super user to log in as by doing: `python manage.py createsuperuser`

## Database Backup and Restoration
There is a Kubernetes CronJob that will automatically do a pg_dump of the database every day.

A backup can then be restored as follows:

```bash
# Create a database to restore into.
dropdb [DBNAME]
createdb [DBNAME]

# If the dump file has a different DB user listed, replace with correct one:
sed -i 's/old_user/new_user/g' [FILENAME]
psql -d [DBNAME] -f [FILENAME]

# If any sequence numbers are not starting at the correct value, they can be
# reset as follows:
psql
ALTER SEQUENCE user_id_seq RESTART 3;
```

Alternatively, use pg_restore if the dump file is not a plain-text script.
