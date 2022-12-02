## ----------------------------------------------------------------------
## This is the Web3 Makefile.
##
## Here, we define the Web3 Backend targets to be executed in the
## development flow.
##
## Help comments are displayed in the order defined within the Makefile.
## ----------------------------------------------------------------------
##

_GREEN='\033[0;32m'
_NC='\033[0m'

define log
	@printf "${_GREEN}$(1)${_NC}\n"
endef


# List from https://github.com/docker/cli/issues/1534
CHECK_COMPOSE_PLUGIN := $(shell \
(test -e $(HOME)/.docker/cli-plugins/docker-compose) || \
(test -e /usr/local/lib/docker/cli-plugins/docker-compose) || \
(test -e /usr/lib/docker/cli-plugins/docker-compose) || \
(test -e /usr/libexec/docker/cli-plugins/docker-compose) 2> /dev/null; echo $$?)
COMPOSE_FILE_OPT = -f ./docker/docker-compose.yaml
ifeq ($(CHECK_COMPOSE_PLUGIN), 0)
    DOCKER_COMPOSE_CMD = docker compose $(COMPOSE_FILE_OPT)
else
    DOCKER_COMPOSE_CMD = docker-compose $(COMPOSE_FILE_OPT)
endif

# List available targets
#
# Executing this target is always the recommended
# method for listing the available targets.
#
# However, for platforms with bash-completion
# package installed this can be done automatically
# with tab completion:
# > make 'space' 'tab' tab'
#
# Reference: https://stackoverflow.com/questions/4219255/
help:
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

cp-env: ## Copy docker .env file
	$(call log, Coping env file...)
	cp ./docker/.env.example ./docker/.env

build:
	DOCKER_BUILDKIT=1 sudo $(DOCKER_COMPOSE_CMD) build

up: ## Start docker-defined services, can be passed specific service(s) to only start those. Usage: make up services="mongo backend"
	$(call log, Starting services...)
	$(DOCKER_COMPOSE_CMD) up $(services)

logs: ## Tail logs for a service. Usage: make logs service="backend"
	$(call log, Tailing of logs for service...)
	$(DOCKER_COMPOSE_CMD) logs -f '$(service)'

ps: ## Show containers status
	$(call log, Showing containers status...)
	$(DOCKER_COMPOSE_CMD) ps

rm-volumes: ## Remove old volumes
	$(call log, Removing old volumes...)
	$(DOCKER_COMPOSE_CMD) rm -v

stop: ## Stop containers
	$(call log, Stopping containers...)
	$(DOCKER_COMPOSE_CMD) stop

down: ## Stop and remove containers
	$(call log, Stopping and removing containers...)
	$(DOCKER_COMPOSE_CMD) down

cop: ## Run precommit hooks
	$(call log, Running precommit hooks...)
	$(DOCKER_COMPOSE_CMD) run --rm backend poetry run nox -s cop


restart-backend: ## Restart the backend
	$(call log, Restarting the backend...)
	$(DOCKER_COMPOSE_CMD) restart backend

hasura-cli: ## Hasura command-line interface
	$(call log, Using hasura-cli...)
	$(DOCKER_COMPOSE_CMD) exec -w /code/hasura graphql-engine hasura-cli migrate create