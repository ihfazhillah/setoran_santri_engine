from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required
from setoran_models import *
from .forms import SantriForm


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

@mod.route("/edit/<id_>", methods=["POST"])
@login_required
def edit(id_):
    santri_form = SantriForm()

    if santri_form.validate_on_submit():
        nama = santri_form.nama.data
        with db_session:
            santri = get(s for s in Santri if s.id == id_)
            santri.nama = nama
            flash("Santri with id %s was edited." %id_, 'info')
            return redirect(url_for("front_page.index"))
    flash("%s: %s" %(santri_form.nama.name, santri_form.nama.errors))
    return redirect(url_for("front_page.index"))

@mod.route("/add", methods=["POST"])
@login_required
def add():
    return ""
