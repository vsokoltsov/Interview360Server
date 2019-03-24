## Installation

For starting the virtualbox execute:

* `vagrant up`
* `vagrant vbguest`
* `vagrant reload`

Then, connect to VM via `vagrant ssh` and then execute

* `cd ~/im`
* `pip install -r requirements.txt`
* `cd ~/im/app`
* `pm migrate`

## Environment variables

* create `settings.yml` file with the same keys as `.env.sample`in the root.

## Run server

* `pm runserver 0.0.0.0:8080`

## Testing

* `pm test <path to test> -s`

## Continuous Integration (CircleCI)

* Rename `circle.vagrant.yml` file to `circle.yml`
* Create pull-request and wait for the check.

## Deploy

First, you need to set up a destination ip for the deploy in `fabfile.py`.

### Provision

* `fab provision`

### Deployment

* `fab deploy`

