include .envrc

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

# ============================================================================ #
# DATABASE
# ============================================================================ #

## db/psql: Connect to the database using psql
.PHONY: db/psql
db/psql:
	psql ${FT_DB_DSN}

## db/sqlite: Connect to the database using sqlite
.PHONY: db/sqlite
db/sqlite:
	sqlite3 ${FT_DB_DSN}

## db/makemigrations: Create a new migration based on any recent model changes
.PHONY: db/makemigrations app=$1
db/makemigrations:
	@echo "Making a new database migration..."
	python3 app/manage.py makemigrations ${app}

## db/migrate: Apply the latest database migrations
.PHONY: db/migrate
db/migrate:
	@echo "Applying latest database migrations..."
	python3 app/manage.py migrate

# ============================================================================ #
# BUILD
# ============================================================================ #

## build/api: Build the cmd/api application
.PHONY: build/app
build/app:
	@echo "Building app from Dockerfile"
	$(CONTAINER_CMD) build -t docker.io/mijoap/fitness-tracker:latest .
