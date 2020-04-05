import time

import click
import flask
import flask.cli
import sqlalchemy as sa
import sqlalchemy.exc

from . import db
from . import models


# Actual DB initialisation - schema + data:

def initialize_db(
    engine: sa.engine.Engine,
    *,
    force_drop_known: bool = False,
    force_nuke_whole_db: bool = False,  # Dangerous as hell!
):
    initialize_db_schema(
        engine,
        force_drop_known=force_drop_known,
        force_nuke_whole_db=force_nuke_whole_db,
    )


# DB schema initialization:

def nuke_db(engine :sa.engine.Engine):
    reflected_metadata = sa.MetaData(
        bind=engine,
        reflect=True
    )
    reflected_metadata.drop_all()


def initialize_db_schema(
    engine :sa.engine.Engine,
    *,
    force_drop_known :bool = False,
    force_nuke_whole_db :bool = False,  # Dangerous as hell!
):
    # TODO add option for transactional DDL

    if force_nuke_whole_db:
        nuke_db(engine)
    if force_drop_known:
        # For most case this could be an elif,
        #  unless we're issuing some custom DDL that
        #  have defined drop events but cannot be reflected.
        models.base.metadata.drop_all(engine)

    models.base.metadata.create_all(engine)


# Utils:

def wait_for_db(
    engine :sa.engine.Engine,
    num_retries = 5,
    linear_backoff_secs = 2,
):
    wait_secs = 0
    while True:
        num_retries -= 1
        wait_secs += linear_backoff_secs
        try:
            with engine.connect():
                return
        except sa.exc.OperationalError:
            if num_retries:
                print(
                    f"Waiting for DB to accept connections, retrying {num_retries}"
                    f" more times in {wait_secs} seconds..."
                )
                time.sleep(wait_secs)
            else:
                raise


# Entry point:

@click.command()
@click.option('--drop-known', is_flag=True)
@click.option('--drop-all-reflected', is_flag=True)
@flask.cli.with_appcontext
def init_db(drop_all_reflected, drop_known):
    app_config = flask.current_app.config
    engine = db.boilerplate.get_engine(app_config['DB_CONFIG'])

    wait_for_db(engine)  # Because Docker Compose.

    # TODO support transactional DDL.
    initialize_db(
        engine,
        force_drop_known=drop_known,
        force_nuke_whole_db=drop_all_reflected,
    )


def setup_on_app(app :flask.Flask):
    app.cli.add_command(init_db)
