from flask import Flask
from hatchet import Environment


def test_app_is_flask(app):
    assert isinstance(app, Flask)


def test_app_is_testing_config(app):
    assert app.config.get("ENV") == Environment.TEST


def test_app_has_sqlalchemy_connection_string(app):
    assert app.config.get("SQLALCHEMY_DATABASE_URI") == "sqlite:///:memory:"
