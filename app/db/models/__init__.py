from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship

from app.db import db


class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    artist = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="songs", uselist=False)

    def __init__(self, title, artist, year, genre):
        self.title = title
        self.artist = artist
        self.year = year
        self.genre = genre


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    is_admin = db.Column(db.Boolean(), nullable=False, server_default="0")
    songs = db.relationship("Song", back_populates="user", cascade="all, delete")

    def __init__(self, username, password, about):
        self.username = username
        self.password = password
        self.about = about

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active
