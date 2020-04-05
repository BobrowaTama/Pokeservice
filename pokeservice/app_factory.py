import os

import flask

from . import config
from . import db
from . import views
from . import cli


def get_instance_path_from_env():
    # Why doesn't Flask have a functionality to specify this using the CLI OOTB?...
    return os.environ.get('POKESERVICE_FLASK_INSTANCE_DIR')


def load_config(app :flask.Flask, test_config):
    # First read defaults from package
    defaults = config.Defaults()
    app.config.from_object(defaults)

    # Then apply overrides from instance-level config file
    app.config.from_pyfile('pokeservice.cfg.py')
    
    if test_config:
        app.config.from_mapping(test_config)


def create_app(test_config=None):
    instance_path = get_instance_path_from_env()

    # Flask initialisation
    app = flask.Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True,
    )

    load_config(app, test_config)

    # "Inverted" initialisation flow - allow components to "setup themselves" on the app
    #  instead of taking care of all bits and pieces from one place.
    # This approach is loosely inspired by Pyramid's includeme() functions.

    db.setup_on_app(app)
    views.setup_on_app(app)
    cli.setup_on_app(app)

    return app
