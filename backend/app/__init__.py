from flask import Flask
from flask_cors import CORS
from .db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    with app.app_context():
        from .routes import register_routes
        register_routes(app)
        db.create_all()

    return app