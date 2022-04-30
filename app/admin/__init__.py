from flask import Blueprint, render_template
from flask_login import login_required

from app.auth.decorators import admin_required
from app.admin.forms import DeleteForm, AddForm, EditForm
from app.db.models import User

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def index():
    delete_form = DeleteForm()
    users = User.query.order_by(User.id).all()
    results = [{
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "about": user.about,
    } for user in users]

    return render_template("admin.html", results=results, delete_form=delete_form)
