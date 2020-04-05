#!/usr/bin/env bash

set -e

function usage_err() {
	echo >&2 "Usage: $0 <target_config_set_name> [init_db flags...]"
	exit 1
}

TARGET_CONFIG_SET_NAME="$1"
shift || usage_err
export TARGET_CONFIG_SET_NAME

eval $(docker-machine env "$TARGET_CONFIG_SET_NAME")

docker-compose build
docker-compose run web env FLASK_APP=pokeservice flask init_db "$@"
