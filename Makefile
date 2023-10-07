include .envrc

FT_APP_NAME=fitness-tracker
FT_CONTAINER_IMAGE_TAG=1.0.0
FT_CONTAINER_IMAGE_APP=${CONTAINER_REGISTRY}/${CONTAINER_REGISTRY_USER}/${FT_APP_NAME}:${FT_CONTAINER_IMAGE_TAG}
FT_CONTAINER_IMAGE_PROXY=${CONTAINER_REGISTRY}/${CONTAINER_REGISTRY_USER}/${FT_APP_NAME}-proxy:${FT_CONTAINER_IMAGE_TAG}

# ============================================================================ #
# HELPERS
# ============================================================================ #

## help: Print this help message
.PHONY: help
help:
	@echo "Usage:"
	@sed -n "s/^##//p" ${MAKEFILE_LIST} | column -t -s ":" | sed -e "s/^/ /"

.PHONY: confirm
confirm:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

# ============================================================================ #
# DEVELOPMENT
# ============================================================================ #

## manage command=$1: Run the Django manage.py script with the given command
.PHONY: manage command=$1
manage:
	python3 app/manage.py ${command}

## shell: Run the Django interactive command shell
.PHONY: shell
shell:
	python3 app/manage.py shell

## run: Run the Django development server
.PHONY: run port=$1
run:
	python3 app/manage.py runserver ${port}

## run/container: Enter the fitness-tracker container image
.PHONY: run/container
run/container:
	@echo "Entering the fitness-tracker container"
	${CONTAINER_CMD} container run \
		--rm -it \
		--name fitness-tracker \
		-e FT_DEBUG=${FT_DEBUG} \
		-e FT_SECRET_KEY=${FT_SECRET_KEY} \
		-e FT_DB_ENGINE=${FT_DB_ENGINE} \
		-e FT_DB_HOST=${FT_DB_HOST} \
		-e FT_DB_PORT=${FT_DB_PORT} \
		-e FT_DB_USERNAME=${FT_DB_USERNAME} \
		-e FT_DB_PASSWORD=${FT_DB_PASSWORD} \
		-e FT_DB_NAME=${FT_DB_NAME} \
		${FT_CONTAINER_IMAGE} \
		sh

# ============================================================================ #
# DATABASE
# ============================================================================ #

## db/psql: Connect to the database using psql
.PHONY: db/psql
db/psql:
	@PGPASSWORD=${FT_DB_PASSWORD} \
	psql \
		--host ${FT_DB_HOST} \
		--port ${FT_DB_PORT} \
		--dbname ${FT_DB_NAME} \
		--username ${FT_DB_USERNAME}

## db/sqlite: Connect to the database using sqlite
.PHONY: db/sqlite
db/sqlite:
	sqlite3 app/${FT_DB_NAME}

## db/makemigrations: Create new migrations based on any recent model changes
.PHONY: db/makemigrations app=$1
db/makemigrations:
	@echo "Making new database migrations..."
	python3 app/manage.py makemigrations ${app}

## db/migrate: Apply the latest database migrations
.PHONY: db/migrate
db/migrate:
	@echo "Applying latest database migrations..."
	python3 app/manage.py migrate

# ============================================================================ #
# BUILD
# ============================================================================ #

## collectstatic: Copy all static files to the proxy directory
.PHONY: collectstatic
collectstatic:
	python3 app/manage.py collectstatic

## build/login: Log in to the container registry with an access token
.PHONY: build/login
build/login:
	@echo "Logging in to the container registry with access token"
	@${CONTAINER_CMD} login ${CONTAINER_REGISTRY} \
		--username ${CONTAINER_REGISTRY_USER} \
		--password ${CONTAINER_REGISTRY_ACCESS_TOKEN}

## build/container/app: Build the application container image and push it to the registry
.PHONY: build/container/app
build/container/app:
	@echo "Building app from Containerfile"
	${CONTAINER_CMD} image build -t ${FT_CONTAINER_IMAGE_APP} app/
	@echo "Pushing built container image to ${FT_CONTAINER_IMAGE_APP}"
	${CONTAINER_CMD} image push ${FT_CONTAINER_IMAGE_APP}

## build/container/proxy: Build the proxy container image and push it to the registry
.PHONY: build/container/proxy
build/container/proxy:
	@echo "Building proxy from Containerfile"
	${CONTAINER_CMD} image build \
		--build-arg NGINX_SERVER_NAME=${NGINX_SERVER_NAME} \
		-t ${FT_CONTAINER_IMAGE_PROXY} \
		proxy/
	@echo "Pushing built container image to ${FT_CONTAINER_IMAGE_PROXY}"
	${CONTAINER_CMD} image push ${FT_CONTAINER_IMAGE_PROXY}

# ============================================================================ #
# DEPLOY
# ============================================================================ #

## deploy: Deploy the application to the given Kubernetes cluster
.PHONY: deploy env=$1
deploy:
	@echo "Generating YAML patches from template files"
	sed "s|FT_CONTAINER_IMAGE_APP|${FT_CONTAINER_IMAGE_APP}|g" kustomize/overlays/${env}/patch_app.yaml.tmpl > kustomize/overlays/${env}/patch_app.yaml
	sed "s|NGINX_SERVER_NAME|${NGINX_SERVER_NAME}|g" kustomize/overlays/${env}/patch_ingress.yaml.tmpl > kustomize/overlays/${env}/patch_ingress.yaml
	sed "s|FT_CONTAINER_IMAGE_PROXY|${FT_CONTAINER_IMAGE_PROXY}|g" kustomize/overlays/${env}/patch_proxy.yaml.tmpl > kustomize/overlays/${env}/patch_proxy.yaml
	@echo "Deploying to Kubernetes cluster"
	kubectl apply --kustomize kustomize/overlays/${env}/
	@echo "Cleaning up YAML patches"
	@rm kustomize/overlays/${env}/patch_app.yaml
	@rm kustomize/overlays/${env}/patch_ingress.yaml
	@rm kustomize/overlays/${env}/patch_proxy.yaml
