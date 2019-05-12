import os

from hatchet import Environment


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/api/v1/swagger'
    OPENAPI_PATH = '/static/swagger/openapi.yml'

    @classmethod
    def get(cls, env: str):
        config_map = {
            'prd': ProductionConfig,
            'dev': DevelopmentConfig,
            'test': TestingConfig
        }
        return config_map.get(env)


class DevelopmentConfig(Config):
    RESTART_ON_CHANGE = True
    ENV = Environment.DEV0
    DEBUG = True
    CREATE_SCHEMA = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.getcwd()}/data.sqlite'
    #SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(Config):
    RESTART_ON_CHANGE = False
    ENV = Environment.PROD
    DEBUG = False
    CREATE_SCHEMA = False


class TestingConfig(Config):
    RESTART_ON_CHANGE = False
    ENV = Environment.TEST
    DEBUG = False
    CREATE_SCHEMA = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///:memory:'


