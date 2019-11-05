import pytest
from hatchet.app import create_app


@pytest.fixture
def app():
    app = create_app("test")
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()
