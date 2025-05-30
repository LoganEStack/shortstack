from flask import Flask
from flask_cors import CORS
from config import Config

from .routes import main
from .routes_db import admin
from .db import db
from .limiter import limiter, register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "https://frontend-6oxa.onrender.com"}}, supports_credentials=True)
    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    limiter.init_app(app)
    register_error_handlers(app)

    return app

app = create_app()