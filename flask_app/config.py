import os
import redis

basedir = os.path.abspath(os.path.dirname(__file__))


class PostgreConfig:
    POSGRE_IP = os.getenv('POSTGRE_IP')
    POSGRE_USERNAME = os.getenv('POSTGRE_USERNAME')
    POSGRE_DB = os.getenv('POSTGRE_DB')
    POSGRE_PASSWORD = os.getenv('POSTGRE_PASSWORD')


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'jkndjffdjjkr'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    # SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://' \
    #                           f'{PostgreConfig.POSGRE_USERNAME}:{PostgreConfig.POSGRE_PASSWORD}' \
    #                           f'{PostgreConfig.POSGRE_IP}/{PostgreConfig.POSGRE_DB}'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    REDIS_HOST = "redis"
    REDIS_PORT = 6379

    AppId = os.getenv('APPID')
    AppSecret = os.getenv('APP_SECRET')


class DevelopConfig(Config):
    pass


class ProductConfig(Config):
    DEBUG = False


config_map = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
