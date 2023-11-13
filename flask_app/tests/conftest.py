import pytest
from mongomock import MongoClient

from server import app as flask_app
from db import MongoDBConnection


# Configuração do banco de dados mock
@pytest.fixture(scope="function")
def mongo_mock():
    MongoDBConnection.client = MongoClient()
    yield
    MongoDBConnection.client = None


@pytest.fixture
def app():
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
