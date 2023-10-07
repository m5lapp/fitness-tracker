# fitness-tracker
A very simple web application for tracking fitness progress into a SQL database. Developed using Django's admin interface.

## Local Development
For local development, create a .envrc file with the following content and load it with `source .envrc`. Replace any UPPER_CASE_PLACEHOLDERS with appropriate values.

```bash
export CONTAINER_CMD=podman

# Container registry details required for pushing and possibly pulling images.
export CONTAINER_REGISTRY=docker.io
export CONTAINER_REGISTRY_ACCESS_TOKEN='REGISTRY_ACCESS_TOKEN'
export CONTAINER_REGISTRY_USER=REGISTRY_USER_NAME

# Build environment variables.
export NGINX_SERVER_NAME=fitness-tracker.example.com

# Development application environment variables. If using SQLite, then only the
# FT_DB_ENGINE and FT_DB_NAME database variables are required.
export FT_ALLOWED_HOSTS=127.0.0.1,localhost
export FT_DB_ENGINE=sqlite3
export FT_DB_NAME=app/db.sqlite3
export FT_DB_HOST=db.example.com
export FT_DB_PORT="5432"
export FT_DB_USERNAME=fitness_tracker_dev_user
export FT_DB_PASSWORD=Sup3rS3cr3tP455w0rd

export FT_DEBUG=1
export FT_SECRET_KEY='abcdefghijklmnopqrstuvwxyz0123456789'
```

You can then perform various tasks with the targets in the Makefile such as running a development server, accessing a Django shell, running management commands and creating database migrations. You can see a complete list of the available commands by running `make help`.

## Deployment
### Build the Container Images
1. Update the FT_CONTAINER_IMAGE_TAG version number at the top of the `Makefile`
1. Copy all the static files to the proxy directory: `make collectstatic`
1. Log in to the container registry: `make build/login`
1. Build and push the proxy and application container images:
    1. `make build/container/proxy`
    1. `make build/container/app`

### Deploy to Kubernetes
The YAML provided in the `kustomize/` directory can be used to deploy the application to a Kubernetes cluster as follows. If you want to deploy to an environment other than production, duplicate the `kustomize/overlays/prod/` directory and give it an appropriate name. You can then follow the steps below in that directory rather than the `prod/` one.

1. Create the two files listed below in the `prod/` directory with appropriate values; do not surround the values in quotes of any kind
1. Generate and deploy the Kubernetes manifests by running `make deploy env=prod` where `prod` is the name of the environment directory in the `kustomize/overlays/` directory
1. If the application is running for the very first time, you will need to create a super user to log in as by running: `kubectl exec -it -n fitness-tracker -c fitness-tracker deployment/fitness-tracker -- python manage.py createsuperuser`

#### kustomize/overlays/prod/data_configmap.properties
```bash
FT_ALLOWED_HOSTS=fitness-tracker,localhost
FT_CSRF_TRUSTED_ORIGINS=https://fitness-tracker.example.com,http://localhost
FT_DB_ENGINE=postgresql
FT_DB_PORT=5432
FT_DEBUG=0
```
#### kustomize/overlays/prod/data_secret.properties
```bash
FT_DB_HOST=db.example.com
FT_DB_NAME=fitness_tracker
FT_DB_PASSWORD=Sup3rS3cr3tP455w0rd
FT_DB_USERNAME=fitness_tracker
FT_SECRET_KEY=abcdefghijklmnopqrstuvwxyz0123456789
```

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
