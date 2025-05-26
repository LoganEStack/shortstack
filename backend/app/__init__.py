from flask import Flask
from config import Config
from .routes import main
from .routes_debug import debug
from .db import db
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(debug)

    with app.app_context():
        db.create_all()

    return app
