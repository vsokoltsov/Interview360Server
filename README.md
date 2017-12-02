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

* Django server with `ipdb` debug - `docker-compose run --service-ports web python app/manage.py runserver 0.0.0.0:80`
* Watching logs of other services - `docker-compose logs -f`

## Run tests

* `pm test <path to test> -s`

* Create file `secrets.yaml` in `/app/app` folder, where all your environment variables would be allocated
