import pytest

import pokeservice
import pokeservice.cli
import pokeservice.db


@pytest.fixture
def app():
    app = pokeservice.create_app({'TESTING': True})
    return app


@pytest.fixture
def recreate_db(app):
    db_config = app.config['DB_CONFIG']

    if not db_config.get('this_is_testing_db_that_can_be_dropped_in_its_entirety'):
        # That was close!
        raise ValueError("You aren't testing on production, are you?")
    else:
        engine = pokeservice.db.boilerplate.get_engine(db_config)

        pokeservice.cli.initialize_db(
            engine,
            force_drop_known=True,
            force_nuke_whole_db=True,
        )
