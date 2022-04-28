from flask import Blueprint, render_template
from app.db.models import User

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/admin", methods=["GET"])
def index():
    users = User.query.order_by(User.id).all()
    results = [{
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "about": user.about,
        "songs": user.songs.__dict__
    } for user in users]

    return render_template("admin.html", results=results)
