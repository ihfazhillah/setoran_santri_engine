from flask import Flask
from setoran_models import *
# from db_config import db 

from webmodules.index.routes import mod as front_page_mod

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.register_blueprint(front_page_mod)

    return app
