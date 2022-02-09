from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.future.engine import create_engine 
from flask import Flask, _app_ctx_stack, render_template
from micawber.cache import Cache
from micawber import bootstrap_basic
from flask_msearch import Search

db = SQLAlchemy()
_bcrypt = Bcrypt()
login_manager = LoginManager()
oembed_providers = bootstrap_basic(Cache)
_search = Search()
Session = sessionmaker()

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
    
    # Initialise Flask FTS module
    _search.init_app(app)

    # Initialise database session
    Session.configure(bind=create_engine(app.config['SQLALCHEMY_DATABASE_URI']))

    with app.app_context():
        from .auth import bp as auth_bp
        from .main import bp as main_bp
        from .models import User

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        app.session = scoped_session(Session, scopefunc=_app_ctx_stack.__ident_func__)

        db.create_all()

        login_manager.login_view = "auth.login"

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        @app.teardown_appcontext
        def remove_session(*args, **kwargs):
            app.session.remove()

        @app.route("/", methods=["GET"])
        def hello():
            return render_template("hello.html")

    return app
