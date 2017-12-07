[![CircleCI](https://circleci.com/gh/vforvad/Interview360Server.svg?style=svg)](https://circleci.com/gh/vforvad/Interview360Server)

## Interview Manager App

Service for managing employees interview workflow

For start application you will need:

## Installation

### Vagrant

* `vagrant up`
* `vagrant vbguest`
* `vagrant reload`

Then, connect to VM via `vagrant ssh` and then execute

* `cd ~/im`
* `pip install -r requirements.txt`
* `cd ~/im/app`
* `pm migrate`

### Docker

* `docker-compose up`
* in another terminal `docker-compose run --rm db bash`
* `psql -U postgres`
* `CREATE DATABASE interview_manager;`

## Run server

### Vagrant

* `pm runserver 0.0.0.0:8080`

### Docker

* Django server with `ipdb` debug - `docker-compose run --service-ports --rm web python app/manage.py runserver 0.0.0.0:80`
* Watching logs of other services - `docker-compose logs -f`

*Notice*: The `vm.max_map_count` kernel of `elasticsearch` setting needs to be set to at least
262144 for production use. Depending on your platform:
* docker-machine ssh
* sudo sysctl -w vm.max_map_count=262144

## Run tests

### Vagrant:
* `pm test <path to test> -s`

### Docker

* `docker-compose run --rm app bash -c "cd app && python manage.py test"`

* Create file `secrets.yaml` in `/app/app` folder, where all your environment variables would be allocated
