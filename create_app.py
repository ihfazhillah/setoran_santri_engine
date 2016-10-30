from flask import Flask
from setoran_models import *
# from db_config import db 


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from flask_login import LoginManager
    from webmodules.auth.helpers import User, USERS

    lm = LoginManager(app)
    lm.login_view = "auth.login"
    lm.login_message = "You're not logged in"
    lm.login_message_category = "warning"

    @lm.user_loader
    def load_user(userid):
        for user in USERS:
            if user.id == int(userid):
                return user

    from webmodules.index.routes import mod as front_page_mod
    from webmodules.santri.routes import mod as santri_mod
    from webmodules.auth.routes import mod as auth_mod
    from webmodules.setoran.routes import mod as setoran_mod 

    app.register_blueprint(front_page_mod)
    app.register_blueprint(santri_mod, url_prefix="/santri")
    app.register_blueprint(auth_mod, url_prefix="/auth")
    app.register_blueprint(setoran_mod, url_prefix="/setoran")

    return app
