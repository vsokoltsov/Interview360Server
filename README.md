[![CircleCI](https://circleci.com/gh/vsokoltsov/Interview360Server.svg?style=svg)](https://circleci.com/gh/vsokoltsov/Interview360Server)

## Interview Manager App

Service for managing employees interview workflow.

## Setup

* Generate `.env` file according to the .env.sample file
* For deployment
  * Generate `.env.prod` file for necessary environment variables
  * Generate `dev.conf` file in `deploy/nginx` folder according to the `development.conf.example`

More information about environment variables you can find (here)[./docs/ENV.md]

## Application settings

There are two main options of running and working with application:

* [Vagrant](./docs/VAGRANT.md)
* [Docker](./docs/DOCKER.md)

Another options:

* In order to run [silk](https://github.com/jazzband/django-silk) you need to collect
static files via `python manage.py collectstatic` and pass `--silk-enabled` argument for
`runserver`


* Dump database
  * For local development (I am using OS X ) you should apply these steps:
    * Create dump `docker-compose exec pg_dump -U postgres -h db interview_manager > <dump name>.sql`
    * Copy dump to docker machine environment `docker-machine scp ./<dump name> default:/var/lib`
    * Move dump on docker machine to folder which is volume to the `db` container
      (`/var/lib/postgresql/data` in my case)
    * Move to database container, to folder where dump is present
    * Type `psql -U postgres -h db interview_manager < <dump name>`
