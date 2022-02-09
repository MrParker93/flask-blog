from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect
from micawber.cache import Cache
from micawber import bootstrap_basic

db = SQLAlchemy()
_bcrypt = Bcrypt()
login_manager = LoginManager()
oembed_providers = bootstrap_basic(Cache)

def create_app(config_setting):
    """Construct the core application."""
    app = Flask(__name__)

    # Sets app configuration based on FLASK_ENV value
    config_module = f"config.{config_setting.capitalize()}Config"
    app.config.from_object(config_module)

    # Initialise LoginManager
    login_manager.init_app(app)

    # Initialise Bcrypt extension
    _bcrypt.init_app(app)

    # Initialise the database
    db.init_app(app)

    with app.app_context():
        from .auth import bp as auth_bp
        from .main import bp as main_bp
        from .models import User

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        db.create_all()

        login_manager.login_view = "auth.login"

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.route("/", methods=["GET"])
        def hello():
            return render_template("hello.html")

    return app
