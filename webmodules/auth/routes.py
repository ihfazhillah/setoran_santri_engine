from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_user 
from .forms import LoginForm
from .helpers import User

mod = Blueprint("auth", __name__, template_folder="templates")


@mod.route("/login", methods=['POST', 'GET'])
def login():
    login_form = LoginForm(csrf_enabled=False)

    if request.method == 'POST':
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data

            user = User(username, password)

            if user.is_authenticated:
                login_user(user)
                flash("Login Success")
                return redirect(url_for("front_page.index"))

            flash("Wrong username or password.", "warning")
            


    return render_template("auth/login.html",
                           login_form=login_form)
