## Default environment

Here are the keys which are necessary for the all environments

### Required

Required base keys. Without them application will not work correctly. If you  miss
one of the variable, you will be notified by the exception that will tell,
which exact variable is missed.

* `SECRET_KEY` - salt string for the encryption process
* `DEFAULT_CLIENT_HOST` - Used for the email sending. Default - `http://localhost:4200`
* `HOST` - Name for the docker container, which represents the database. Default - `database`
* `USER` - Name of the Postgres user. Default - `postgres`
* `PASSWORD` - Password for the Postgres user. Default - `postgres`

### Optional

Optional environment variables. Use them as a flag for specific service.

* `MAILGUN_API_KEY` - API key from [Mailgun](https://www.mailgun.com/) service
* `MAILGUN_SERVER_NAME` -Server domain from [Mailgun](https://www.mailgun.com/) service
* `ELASTICSEARCH_URL` - URL of the [Elasticsearch](https://www.elastic.co/) container
* `ELASTIC_PASSWORD` - Password for the [Kibana](https://www.elastic.co/products/kibana) authentication
* `RABBITMQ_DEFAULT_USER` - Name of user who will be acessing to the [RabbitMQ](https://www.rabbitmq.com/) service
* `RABBITMQ_DEFAULT_PASS` - Password of user who will be acessing to the [RabbitMQ](https://www.rabbitmq.com/) service
* `TWILIO_ACCOUNT_SID` - Secret key from [Twilio](https://www.twilio.com/) account
* `TWILIO_AUTH_TOKEN` - Authorization token from [Twilio](https://www.twilio.com/) account
* `GOOGLE_PLACES_API` - API key from [Google Places](https://cloud.google.com/maps-platform/places/)
* `DISABLE_FILE_LOGGING` - Flag for disabling the filelogs, which will be stored in `app/app/logs` folder

## Provider-base environments

Environment variables for using some cloud-based services

### [AWS](https://aws.amazon.com)

* `AWS_KEY` - API key from the AWS credentials
* `AWS_SECRET` - API secret key from the AWS credentials
* `AWS_REGION` - Default AWS user region, where the bucket will be stored
* `S3_BUCKET` - Name of the bucket, which will be used for media storage. Must be unique


### [GCP](https://cloud.google.com/)

*Note* Implement via [Service accounts](https://cloud.google.com/compute/docs/access/service-accounts)

* `GCP_BUCKET_NAME` - Name of the bucket for media files
* `GCP_CREDENTIALS_NAME` - Name of the credentials file. Supposed, that file is located under `app/app/credentials` directory
and has `json` format
