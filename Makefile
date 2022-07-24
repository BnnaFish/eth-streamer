-include .env

# commands
lint: mypy flake8 flake8.tests

mypy:
	@mypy app

flake8:
	@flake8 app

flake8.tests:
	@flake8 --append-config=flake8.tests.ini tests

test:
	@pytest

isort:
	isort --atomic .

# docker: control services
stop:
	@docker-compose stop

down:
	@docker-compose down -v --remove-orphans

# docker: built containers
build.web:
	@docker-compose build web

build.test:
	@docker-compose build test

build.bash:
	@docker-compose build bash

# docker: exec
bash:
	@docker-compose run bash sh

# docker: commands
dc.isort: build.bash
	@docker-compose run bash make isort;

dc.flake8: stop build.test
	@docker-compose run test make flake8;

dc.lint: stop build.test
	@docker-compose run test make lint;

dc.test: stop build.test
	@docker-compose run test make test;
	@docker-compose run test make lint;
	@docker-compose stop;
