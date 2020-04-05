#!/usr/bin/env python3
import os
import secrets

import cookiecutter.main


def main():
    here = os.path.dirname(os.path.abspath(__file__))

    cookiecutter_dir = here + '/target_config_set_cookiecutter/'
    target_dir = 'docker_configs/'

    os.makedirs(target_dir, exist_ok=True)

    cookiecutter.main.cookiecutter(
        cookiecutter_dir,
        output_dir=target_dir,
        extra_context={
            'pg_password': secrets.token_urlsafe(),
        },
        # no_input=True,
    )


if __name__ == '__main__':
    main()
