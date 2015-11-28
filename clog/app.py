from flask import Flask, make_response, jsonify
from flask.ext.marshmallow import Marshmallow
from flask_limiter import Limiter

from config import get_config


ma = Marshmallow()
limiter = Limiter()


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(get_config())

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return make_response(
            jsonify(error='exceeded ratelimit of {}'.format(e.description)),
            429
        )

    ma.init_app(app)
    limiter.init_app(app)

    from .api_v1 import api
    from .web import web
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(web)

    return app
