from flask import Blueprint, render_template


mod = Blueprint("front_page", __name__,
                template_folder="templates")

@mod.route("/")
def index():
    return render_template("front_page/index.html",
                           sudah_setor="",
                           belum_setor="",
                           setoran="")