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
		python /interview360/app/manage.py shell

.PHONY: dbshell
dbshell:
	@echo "$@"
	docker exec -it interview360 \
		python /interview360/app/manage.py dbshell

.PHONY: migrate
migrate:
	@echo "$@"
	docker exec -it interview360 \
		python /interview360/app/manage.py migrate

.PHONY: debug
debug:
	@echo "$@"
	docker attach  interview360

.PHONY: test
test:
	@echo "$@"
	docker exec -it interview360 \
		python /interview360/app/manage.py test