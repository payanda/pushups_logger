from . import db
from flask_login import UserMixin
from datetime import datetime, timezone

'''--------------------------- Users Table ---------------------------'''
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # add a relationship with Workouts table
    workouts = db.relationship('Workouts', backref='author', lazy=True)
    
'''--------------------------- Workouts Table ---------------------------'''
class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pushup = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    