#!/bin/bash

cp .env.sample .env
docker-compose build db app cache