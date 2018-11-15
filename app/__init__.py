from flask import Flask
from config import app_config
# method that creates out app
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config)
    app.config.from_pyfile('config.py')
    # app.config['BUNDLE_ERRORS'] = True
    # app.config['ERROR_404_HELP'] = False
    # app.url_map.strict_slashes = False

    # register blueprints
    from app.api.v1 import v1

    app.register_blueprint(v1)
    return app