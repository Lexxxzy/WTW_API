
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

""" 
    Модели используемные API для связи с БД
""" 

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    realname = db.Column(db.String(80), nullable=True)
    avatar_URL = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    likes = db.Column(db.Text())
    dislikes = db.Column(db.Text())
    favourites = db.Column(db.Text())
    isAcivated = db.Column(db.Text())
    code = db.Column(db.Integer)
    recomendations = db.Column(db.Text())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class ComingSoon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    genre = db.Column(db.Text())
    ratingKinopoisk = db.Column(db.Text())
    ratingIMDb = db.Column(db.Text())
    date = db.Column(db.Integer)
    description = db.Column(db.Text())
    poster = db.Column(db.Text())
    frames = db.Column(db.Text())
    country = db.Column(db.Text())
    ifSeries = db.Column(db.Text())
    seasons = db.Column(db.Integer)
    dateTo = db.Column(db.Integer)
    age = db.Column(db.Integer)
    tags = db.Column(db.Text())

    def __repr__(self) -> str:
        return 'ComingSoon>>> {self.url}'
