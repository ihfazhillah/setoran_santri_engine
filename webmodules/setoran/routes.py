from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required
from setoran_models import *



mod = Blueprint("setoran", __name__,
                template_folder="templates")

@mod.route("/delete/<int:id_>")
@login_required
def delete(id_):
    pass