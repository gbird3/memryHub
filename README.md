# memryHub

## Development
1. Make sure docker and docker compose are installed.
https://docs.docker.com/compose/install/

1. Run this command `docker volume create pgdata` (it should only be run once, in order to create a persistence location for postgres data)

1. In the command line run
`docker-compose up`

This will build the docker containers and start them on your machine. With that running, you should be able to go to localhost:8000 and see the running app.

#### Migrations

####Collect static
1. To run Django's collectstatic command in Docker, run
`docker-compose run web python manage.py collectstatic`
