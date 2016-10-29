from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required
from setoran_models import *


mod = Blueprint("santri", __name__,
                template_folder="templates")


@mod.route("/display/<id_>")
@db_session
def display(id_):
    santri = get(s for s in Santri if s.id == id_)
    setoran = select(s for s in Setoran if s.santri == santri)
    return render_template("santri/display.html", setoran=setoran, santri=santri)

@mod.route("/delete/<id_>")
@login_required
def delete(id_):
    with db_session:
        santri = get(s for s in Santri if s.id == id_)
        santri.delete()
        flash("Santri with id %s was removed." %id_, 'info')
        return redirect(url_for("front_page.index"))

@mod.route("/edit/<id_>", methods=["POST", "GET"])
@login_required
def edit(id_):
    return ""
