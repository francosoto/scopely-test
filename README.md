# FastApi sample + MariaDB + Redis

## Install

Minimal requirements:
- Docker and docker compose
- git
- In order to run setup.sh, it's not compatible with Windows (just because).

First, you must run setup.sh
```
$sh setup.sh
or
$ ./setup.sh
```

It generates a dot env file copied from sample with same values. They are setted by default, you can modify then depending on the environment. Also, it creates all Docker's images but they are not running, we need to do that manually.

## RUN IT

Just run:
```
$ docker-compose up -d cache db
$ docker-compose --compatibility up -d app
$ docker-compose up -d balancer
```

A consideration is taken into account used platform to run containers:
```
platform: linux/amd64
```
In my case, as I'm using MacOS, I need to define it explicitly.

## TRY IT

Some requests examples:
```
$ curl --location --request POST 'http://localhost:8083/player' \
    --header 'Content-Type: application/json' \
    --data '{"name":"player name test","gold":23455}'

{"id":16,"name":"player name test","gold":23455}
```
```
$ curl --location --request GET 'http://localhost:8083/player/16' \
    --header 'Content-Type: application/json'

{"id":16,"name":"player name test","gold":23455}
```

## Tools

Linter
```
$ docker-compose exec app poetry run black app
```

Style guide tool
```
$ docker-compose exec app poetry run flake8 app
```

## TO DO

- You need to build the docker image when .env file is changed. Is better avoid it (restarting service might be enough).
- Implement a Makefile
- Add some unit tests