import redis
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config_map


db = SQLAlchemy()
redis_store = None

def create_app(config_name):
    app = Flask(__name__)

    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    
    from flask_app import apis_1_0
    app.register_blueprint(apis_1_0.api, url_prefix="/api/v1_0")
	return app
