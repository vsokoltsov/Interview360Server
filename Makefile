DEFAULT_APP_PATH := /interview360/app

.PHONY: up
up: docker-compose.yml
	@echo "$@"
	docker-compose up

.PHONY: down
down: docker-compose.yml
	@echo "$@"
	docker-compose down

.PHONY: shell
shell: 
	@echo "$@"
	docker exec -it interview360 \
			/bin/bash

.PHONY: python_shell
python_shell:
	@echo "$@"
	docker exec -it interview360 \
		python $(DEFAULT_APP_PATH)/manage.py shell

.PHONY: dbshell
dbshell:
	@echo "$@"
	docker exec -it interview360 \
		python $(DEFAULT_APP_PATH)/manage.py dbshell

.PHONY: migrate
migrate:
	@echo "$@"
	docker exec -it interview360 \
		python $(DEFAULT_APP_PATH)/manage.py migrate

.PHONY: debug
debug:
	@echo "$@"
	docker attach  interview360

.PHONY: test
test:
	@echo "$@"
	docker exec -it interview360 \
		python $(DEFAULT_APP_PATH)/manage.py test -s $(DEFAULT_APP_PATH)/$(ARGS)