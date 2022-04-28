import os

from flask import render_template, url_for, redirect, abort, Blueprint, current_app
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.forms import LoginForm, UploadForm, RegisterForm
from app.db import db
from app.db.models import User, Song
from app.helpers import read_csv

users = Blueprint("users", __name__, template_folder="templates")


@users.route("users/", methods=["GET"])
def index():
    return render_template("index.html")


@users.route("/user/create", methods=["POST"])
@admin_required
def create():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        new_user = User(username=register_form.username.data, password=register_form.password.data)
        new_user.about = register_form.about.data
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("admin.index"))

    return render_template("add.html")

    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        form.file.data.save(filepath)
        songs = read_csv(filepath)

        for song in songs:
            s = Song(artist=song["artist"], title=song["title"])
            s.year = song["year"]
            s.genre = song["genre"]
            s.user = current_user
            db.session.add(s)

        db.session.commit()

    user = User.query.filter_by(id=current_user.id).first()

    data = [{
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "year": song.year,
        "genre": song.genre
    } for song in user.songs]

    return render_template("dashboard.html", form=form, data=data, username=user.username)


@users.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        new_user = User(username=register_form.username.data, password=register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=register_form)


@users.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return redirect(url_for('upload'))

    return render_template("upload.html", form=form)


@users.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("auth.login"))

