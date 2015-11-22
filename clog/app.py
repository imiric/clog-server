from flask import Flask
from flask.ext.marshmallow import Marshmallow

from config import get_config


ma = Marshmallow()


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(get_config())

    ma.init_app(app)

    from .api_v1 import api
    from .web import web
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(web)

    return app
