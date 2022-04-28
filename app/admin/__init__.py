from flask import Blueprint, render_template, url_for, redirect

from app.db import db
from app.admin.forms import DeleteForm, AddForm
from app.db.models import User

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/admin", methods=["GET", "POST"])
def index():
    delete_form = DeleteForm()
    add_form = AddForm()
    users = User.query.order_by(User.id).all()
    results = [{
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "about": user.about,
    } for user in users]

    return render_template("admin.html", results=results, delete_form=delete_form, add_form=add_form)


@admin.route("/admin/delete", methods=["POST"])
def delete():

    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        user = User.query.filter_by(username=delete_form.username.data).first()
        if user:
            db.session.delete(user)
            db.session.commit()

    return redirect(url_for("admin.index"))


@admin.route("/admin/create", methods=["POST"])
def create():

    add_form = AddForm()

    if add_form.validate_on_submit():
        user = User(username=add_form.username.data, password=add_form.password.data)
        user.about = add_form.about.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin.index"))
