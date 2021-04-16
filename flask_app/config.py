import os
import redis


class Config:
    DEBUG = True
    SECRET_KEY = 'jhdsfjksfuvchsd54665hdgvbh'
    
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://gwjrl:123456@db/demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = "redis"
    REDIS_PORT = 6379


class DevelopConfig(Config):
    pass


class ProductConfig(Config):
    DEBUG = False


config_map = {
    "develop": DevelopConfig,
    "product": ProductConfig
}
