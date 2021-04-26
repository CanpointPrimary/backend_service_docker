from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config_map
from flask_project.utils.redis_utils import redis_store

db = SQLAlchemy()
# cors = CORS


def create_app(config_name):
    app = Flask(__name__, static_folder="../static", template_folder="..")
    # cors.init_app(app)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)
    redis_store.init_app(app)
    
    from flask_project import apis_1_0
    app.register_blueprint(apis_1_0.api, url_prefix="/api/v1_0")

    return app
