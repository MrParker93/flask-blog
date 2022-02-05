from flask import Flask


# Initializes the app and app configurations
def create_app(config_setting):

    app = Flask(__name__)

    config_module = f'config.{config_setting.capitalize()}Config'

    app.config.from_object(config_module)

    @app.route('/')
    def hello_world():
        return "Hello, World!"

    return app