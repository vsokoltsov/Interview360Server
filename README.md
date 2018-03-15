[![CircleCI](https://circleci.com/gh/vsokoltsov/Interview360Server.svg?style=svg)](https://circleci.com/gh/vsokoltsov/Interview360Server)

## Interview Manager App

Service for managing employees interview workflow.

## Setup

* Generate `.env` file according to the .env.sample file
* For deployment
  * Generate `.env.prod` file for necessary environment variables
  * Generate `dev.conf` file in `deploy/nginx` folder according to the `development.conf.example`

## Application settings

There are two main options of running and working with application:

* [Vagrant](https://github.com/vforvad/Interview360Server/wiki/Vagrant-configuration)
* [Docker](https://github.com/vforvad/Interview360Server/wiki/Docker-configuration)

Another options:

* In order to run [silk](https://github.com/jazzband/django-silk) you need to collect
static files via `python manage.py collectstatic` and pass `--silk-enabled` argument for
`runserver`
