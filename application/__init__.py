from flask_bcrypt import Bcrypt
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
_bcrypt = Bcrypt()

def create_app(config_setting):
    """Construct the core application."""
    app = Flask(__name__)

    # Sets app configuration based on FLASK_ENV value
    config_module = f'config.{config_setting.capitalize()}Config'
    app.config.from_object(config_module)
    
    # Initialise Bcrypt extension
    _bcrypt.init_app(app)

    # Initialise the database 
    db.init_app(app)

    with app.app_context():
        from .auth import bp
        app.register_blueprint(bp)

        db.create_all() 

    @app.route('/')
    def index():
        return render_template('main/index.html')

    return app