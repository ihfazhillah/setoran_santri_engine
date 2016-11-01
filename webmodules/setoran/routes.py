from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from setoran_models import Setoran
from pony.orm import db_session, get


mod = Blueprint("setoran", __name__,
                template_folder="templates")


@mod.route("/delete/<id_>")
@login_required
def delete(id_):
    with db_session:
        setoran = get(s for s in Setoran if s.id == id_)
        santri = setoran.santri
        setoran.delete()

        flash("Setoran with id %s from santri with id %s was removed."
              % (id_, santri.id), "info")

        return redirect(url_for("santri.display", id_=santri.id))


@mod.route("/edit/<id_>")
@login_required
def edit(id_):
    pass
