from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .routes import api

    with app.app_context():
        app.register_blueprint(api, url_prefix='/v1')

    return app
