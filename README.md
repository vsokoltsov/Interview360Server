## Interview Manager App

Service for managing employees interview workflow

For start application you will need:

## Installation

* `vagrant up`
* `vagrant vbguest`
* `vagrant reload`

Then, connect to VM via `vagrant ssh` and then execute

* `cd ~/im`
* `pip install -r requirements.txt`
* `cd ~/im/app`
* `pm migrate`

## Run server

* `pm runserver 0.0.0.0:8080`

## Run tests

* `pm test <path to test> -s`

* Create file `secrets.yaml` in `/app/app` folder, where all your environment variables would be allocated
