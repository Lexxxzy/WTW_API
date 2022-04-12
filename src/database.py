from dataclasses import dataclass
from datetime import datetime
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    avatar_URL = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    likes = db.Column(db.Text())
    dislikes = db.Column(db.Text())
    favourites = db.Column(db.Text())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


@dataclass
class ComingSoon(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    genre = db.Column(db.Text())
    date = db.Column(db.Integer)
    description = db.Column(db.Text())
    poster = db.Column(db.Text())
    frames = db.Column(db.Text())
    country = db.Column(db.Text())
    ifSeries = db.Column(db.Text())
    age = db.Column(db.Integer)
    studio = db.Column(db.Text())


    def __repr__(self) -> str:
        return 'ComingSoon>>> {self.url}'
