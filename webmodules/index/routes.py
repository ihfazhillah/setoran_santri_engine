from flask import Blueprint, render_template
from setoran_models import *
from query_setoran import get_belum_setor


mod = Blueprint("front_page", __name__,
                template_folder="templates")

@mod.route("/")
def index():
    sudah_setor = select(s for s in Santri if s not in get_belum_setor())
    setoran = select(s for s in Setoran).order_by(desc(Setoran.timestamp))[:5]
    return render_template("front_page/index.html",
                           sudah_setor=sudah_setor,
                           belum_setor=get_belum_setor(),
                           setoran=setoran)
