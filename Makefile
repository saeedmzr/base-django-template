# Load STAGE from .env file
STAGE := $(shell grep ^STAGE .env | cut -d '=' -f2)

# Choose compose file based on STAGE
ifeq ($(STAGE),local)
  COMPOSE_FILE := docker-compose.yml
else
  $(error Unknown STAGE value '$(STAGE)' in .env)
endif

.PHONY: build recreate up down stop shell shell_as_root test migrate venv install

build:
	docker compose --env-file .env -f $(COMPOSE_FILE) up --build -d
recreate:
	docker compose --env-file .env -f $(COMPOSE_FILE) up --force-recreate -d
up:
	docker compose --env-file .env -f $(COMPOSE_FILE) up -d
down:
	docker compose --env-file .env -f $(COMPOSE_FILE) down
stop:
	docker compose --env-file .env -f $(COMPOSE_FILE) stop
shell:
	docker compose --env-file .env -f $(COMPOSE_FILE) exec app sh
shell_as_root:
	docker compose --env-file .env -f $(COMPOSE_FILE) exec -u root app sh
test:
	docker compose --env-file .env -f $(COMPOSE_FILE) exec app sh -c "python manage.py test"
migrate:
	docker compose --env-file .env -f $(COMPOSE_FILE) exec app sh -c "python manage.py migrate"
venv:
	python3.12 -m venv venv
install:
	. venv/bin/activate && pip install -r requirements/local.txt