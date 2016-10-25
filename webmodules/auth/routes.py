from flask import Blueprint, render_template
from .forms import LoginForm

mod = Blueprint("auth", __name__, template_folder="templates")


@mod.route("/login", methods=['POST', 'GET'])
def login():
    login_form = LoginForm(csrf_enabled=False)

    return render_template("auth/login.html",
                           login_form=login_form)
