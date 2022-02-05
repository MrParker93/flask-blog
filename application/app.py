from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Initializes the app and app configurations
def create_app(config_setting):

    app = Flask(__name__)

    config_module = f'config.{config_setting.capitalize()}Config'

    app.config.from_object(config_module)

    with app.app_context():
        db.__init__(app)

    @app.route('/')
    def hello_world():
        return "Hello, World!"

    return app