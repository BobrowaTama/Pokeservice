import flask
import flask_sqlalchemy_session
import sqlalchemy
import sqlalchemy.orm


def configure_mappers():
    # Import models and call configure_mappers()
    # - this will validate and resolve relationships to avoid later surprises in runtime.

    from .. import models  # noqa
    sqlalchemy.orm.configure_mappers()


configure_mappers()


# Generic SQLAlchemy session acquisition stuff:

def get_engine(settings, prefix='sa_'):
    return sqlalchemy.engine_from_config(settings, prefix)


def get_session_factory(engine, **session_factory_kwargs):
    return sqlalchemy.orm.sessionmaker(bind=engine, **session_factory_kwargs)


def session_factory_from_config(
    settings,
    prefix='sa_',
    **session_factory_kwargs,
):
    engine = get_engine(settings, prefix)
    session_factory = get_session_factory(engine, **session_factory_kwargs)

    return session_factory


# flask_sqlalchemy_session-specific glue:

def configure_flask_sqlalchemy_session(app :flask.Flask):
    db_config = app.config['DB_CONFIG']
    session_factory = session_factory_from_config(db_config)
    flask_sa_session = flask_sqlalchemy_session.flask_scoped_session(session_factory, app)

    return flask_sa_session

