import pytest
from app import create_app, db
from config import TestConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
    # other setup
        yield app
        db.session.remove()
        db.drop_all()
    # clean up

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()