## Run all services

* `make up`

## Run server

* `make up`

## Debug

* `make up`
* In other terminal - `make attach`

## Environment variables

* create `.env` file with the same keys as `.env.sample`in the root.

## Testing

* `make test ARGS="<path to tests>"` (on running application container)

* Create file `secrets.yaml` in `/app/app` folder, where all your environment variables would be allocated

## Continuous Integration (CircleCI)

* Create pull-request and wait for the check.