from flask import Flask
from setoran_models import *
# from db_config import db 


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from webmodules.index.routes import mod as front_page_mod
    from webmodules.santri.routes import mod as santri_mod
    from webmodules.auth.routes import mod as auth_mod

    app.register_blueprint(front_page_mod)
    app.register_blueprint(santri_mod, url_prefix="/santri")
    app.register_blueprint(auth_mod, url_prefix="/auth")

    return app
