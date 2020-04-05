#!/usr/bin/env bash

echo
echo "Config set setup complete."
echo
echo "CONFIG SETS DO NOT PROVIDE DOCKER ENVIRONMENT SEPARATION, they just facilitate rebuilding the images."
echo "They are intended to work together with docker-machine."
echo
echo "You can create corresponding Docker Machine, e.g.:"
echo "  docker-machine create --driver virtualbox {{ cookiecutter.target_config_set_name }}"
echo "Please remember to set environment variables for remote Docker before use! See output of:"
echo "  docker-machine env {{ cookiecutter.target_config_set_name }}"
echo
echo "Please set TARGET_CONFIG_SET_NAME=\"{{ cookiecutter.target_config_set_name }}\" for Docker commands, e.g.:"
echo "  TARGET_CONFIG_SET_NAME=\"{{ cookiecutter.target_config_set_name }}\" docker-compose build"
echo "  TARGET_CONFIG_SET_NAME=\"{{ cookiecutter.target_config_set_name }}\" docker-compose run"
echo
