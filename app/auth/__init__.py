import os

from flask import render_template, url_for, redirect, abort, Blueprint, current_app, flash
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename

from app.auth.forms import LoginForm, UploadForm, RegisterForm
from app.db import db
from app.db.models import User, Song
from app.helpers import read_csv

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            # flash("Welcome", 'success')
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("auth.dashboard"))
        abort(404, "NOT FOUND!!!!!!!")

    return render_template("login.html", form=login_form)


@auth.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    upload_form = UploadForm()

    if current_user.is_authenticated():

        if upload_form.validate_on_submit():
            filename = secure_filename(upload_form.file.data.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            upload_form.file.data.save(filepath)
            songs = read_csv(filepath)

            for song in songs:
                s = Song(artist=song["artist"],
                         title=song["title"],
                         year=song["year"],
                         genre=song["genre"])
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

        return render_template("dashboard.html", form=upload_form, data=data, username=user.username)

    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        new_user = User(username=register_form.username.data,
                        password=register_form.password.data,
                        about=register_form.about.data)
        db.session.add(new_user)
        db.session.commit()
        if new_user.id == 1:
            new_user.is_admin = 1
            new_user.authenticated = 1
            db.session.add(new_user)
            db.session.commit()
        flash("Congratulations, you are now a registered user!", "success")
        return redirect(url_for("auth.login"), 302)

    return render_template("register.html", form=register_form)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))
