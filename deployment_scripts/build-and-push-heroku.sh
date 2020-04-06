#!/usr/bin/env bash

set -e

function usage_err() {
	echo >&2 "Usage: $0 <heroku_app_name>"
	exit 1
}

heroku_app="$1"
shift || usage_err

set -x

docker build -t heroku-pokeservice-web --target app --build-arg=TARGET_CONFIG_SET_NAME="heroku" .
docker tag heroku-pokeservice-web registry.heroku.com/"$heroku_app"/web
docker push registry.heroku.com/"$heroku_app"/web
