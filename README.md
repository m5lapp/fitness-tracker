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
A Helm chart is supplied in the `helm/` directory for deployment to a Kubernetes cluster. There are a number of optional infrastructure features that can be activated such as ingress and client certificates (mTLS) [using Traefik](https://github.com/m5lapp/k3s-fcos-oci/tree/main/docs) and automated database backups if Postgresql is used as the database.

1. Create the namespace, remove the annotation if you do not wish for th Pods within it to be meshed by Linkerd:
   ```bash
   cat << EOF | kubectl apply -f -
   apiVersion: v1
   kind: Namespace
   metadata:
   name: fitness-tracker
   annotations:
     linkerd.io/inject: enabled
   labels:
     app: fitness-tracker
   EOF
   ```
1. Create a custom values file to override any of the values in the `helm/fitness-tracker/values.yaml` file. The path `helm/custom-values.yaml` is gitignored for this purpose if you wish to use it.
1. Install the Helm chart:
   ```sh
   helm upgrade -i fitness-tracker ./helm/fitness-tracker/ \
       -f helm/custom-values.yaml \
       --wait
   ```

## Database Backup and Restoration
There is a Kubernetes CronJob that will automatically do a pg_dump of the database at the given schedule. A backup can then be restored as follows:

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

Alternatively, use `pg_restore` if the dump file is not a plain-text script.
