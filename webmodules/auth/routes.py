from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_user, login_required, logout_user 
from .forms import LoginForm
from .helpers import USERS, usernames

mod = Blueprint("auth", __name__, template_folder="templates")


@mod.route("/login", methods=['POST', 'GET'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data

            if username in usernames:
                user = USERS[usernames[username]]

                if user.password == password:


                    login_user(user)
                    flash("Login Success")
                    return redirect(url_for("front_page.index"))
                else:
                    flash("Wrong username or password.", "warning")
            
            # if user.is_authenticated:
            else:

                flash("Wrong username or password.", "warning")
            


    return render_template("auth/login.html",
                           login_form=login_form)


@mod.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout success.")
    return redirect(url_for("front_page.index"))
