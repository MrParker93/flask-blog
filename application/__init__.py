from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_setting):
    """Construct the core application."""
    app = Flask(__name__)

    # Sets app configuration based on FLASK_ENV value
    config_module = f'config.{config_setting.capitalize()}Config'
    app.config.from_object(config_module)

    # Initialise the database 
    db.init_app(app)

    with app.app_context():
        db.create_all()
        from .authentication import bp
        app.register_blueprint(bp)

    @app.route('/')
    def hello_world():
        return "Hello, World!"

    return app