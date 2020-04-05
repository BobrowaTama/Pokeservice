import typing as tp
import contextlib
import sqlalchemy as sa
import sqlalchemy.orm
import flask_sqlalchemy_session


@contextlib.contextmanager
def transaction_cm(
    session :sa.orm.Session
) -> tp.ContextManager[None]:

    """Provide a transactional scope around a series of operations."""

    try:
        yield
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@contextlib.contextmanager
def current_request_transaction() -> tp.ContextManager[sa.orm.Session]:
    current_flask_scoped_session = flask_sqlalchemy_session.current_session
    session :sa.orm.Session = current_flask_scoped_session()  # get plain `Session` out of `scoped_session`

    with transaction_cm(session):
        yield session
