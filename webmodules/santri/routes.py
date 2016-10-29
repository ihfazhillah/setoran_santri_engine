from flask import Blueprint, render_template
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
    return "this delete page"
    