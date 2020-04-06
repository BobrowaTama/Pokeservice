# Multistage build:
# https://softwarejourneyman.com/docker-python-install-wheels.html


FROM python:3.8-buster AS base

# make /bin/sh symlink to bash instead of dash:
RUN echo "dash dash/sh boolean false" | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash


# Build container:

FROM base AS build
CMD sh

# Python packaging tools
RUN pip install wheel

# System dependencies
#RUN apk add --no-cache build-base python3-dev postgresql-client postgresql-dev
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 libpq-dev
#RUN pip wheel --wheel-dir=/root/wheels psycopg2

# Dependencies - cache them
COPY requirements-for-docker-build-cache.txt /root/sources/pokeservice/
RUN pip wheel --wheel-dir=/root/wheels -r /root/sources/pokeservice/requirements-for-docker-build-cache.txt

# Project code
COPY . /root/sources/pokeservice
RUN pip wheel --wheel-dir=/root/wheels /root/sources/pokeservice


# Target container:

FROM base AS app
CMD sh

# System dependencies
#RUN apk add --no-cache postgresql-client
RUN apt-get update && apt-get install -y --no-install-recommends libpq5

# Copy built packages
COPY --from=build /root/wheels /root/wheels

# Project from built packages
RUN pip install --no-index --find-links=/root/wheels pokeservice

ENV FLASK_APP=pokeservice POKESERVICE_FLASK_INSTANCE_DIR=/root/pokeservice/instance

ARG TARGET_CONFIG_SET_NAME
COPY docker_configs/${TARGET_CONFIG_SET_NAME}/web_instance_dir $POKESERVICE_FLASK_INSTANCE_DIR

ENV PORT=5000

CMD flask run -h 0.0.0.0 -p $PORT
EXPOSE 5000/tcp
