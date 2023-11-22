FROM python:3.11-slim-bullseye as builder

USER root

WORKDIR /app

# Install commonly used packages
RUN apt-get update
RUN apt-get install -y \
  sudo \
  zsh 

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.5.1
    
# installing project dependencies
RUN pip3 install --upgrade pip; \
  python3 -m pip install --upgrade pip setuptools wheel; \
  pip install poetry==$POETRY_VERSION

COPY app /app/app
COPY pyproject.toml poetry.lock poetry.toml .env /app/
COPY .docker/entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

RUN poetry install --no-root --without test && rm -rf $POETRY_CACHE_DIR
