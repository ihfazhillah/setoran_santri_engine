from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from setoran_models import Setoran, Santri
from pony.orm import db_session, get, select
from .forms import SetoranForm


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


@mod.route("/edit/<id_>", methods=["POST"])
@db_session
@login_required
def edit(id_):
    setoran = get(s for s in Setoran if s.id == id_)
    setoran_form = SetoranForm()
    santries = select((s.id, s.nama) for s in Santri)
    setoran_form.santri.choices = [(str(s[0]), s[1]) for s in santries]

    if setoran_form.validate_on_submit():
        santri_id = int(setoran_form.santri.data)
        santri = get(s for s in Santri
                     if s.id == santri_id)
        setoran.santri = santri
        setoran.start = setoran_form.start.data
        setoran.end = setoran_form.end.data
        setoran.jenis = setoran_form.jenis.data
        setoran.lulus = bool(int(setoran_form.lulus.data))

        flash("Setoran with id %s was modified." % id_, "info")

        return redirect(url_for("santri.display", id_=santri.id))
    return setoran_form.errors


@mod.route("/add", methods=['POST'])
@login_required
def add():
    pass
