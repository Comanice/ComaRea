from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # every user can create multiple notes and by the user_id we can lookup which user created a note
    # forces that we have to give a legit user_id to write a note


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # we need to create a unique key for any user
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    notes = db.relationship('Note')
