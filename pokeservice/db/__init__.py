import flask

from . import boilerplate
from .transaction_cm import current_request_transaction


# Entry point for app factory.

def setup_on_app(app :flask.Flask):
    # Ignore return value, views use `current_request_transaction` context manager.
    boilerplate.configure_flask_sqlalchemy_session(app)
