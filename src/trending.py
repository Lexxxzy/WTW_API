from signal import Sigmasks
from flask import Blueprint
from flask import Blueprint, jsonify
from requests import request
from src.constants.http_errors import *
from src.database import ComingSoon
from flask_jwt_extended import jwt_required, get_jwt_identity
from .constants.http_status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from .static.favouriteFilms import FavouriteFilm

trending = Blueprint("trending", __name__, url_prefix="/api/v1/trending")


@trending.get('/')
def get_favourites():
    coming_soon = ComingSoon.query.all()

    finalJSON = []

    for movie in coming_soon:
        finalJSON.append({
            'id': movie.id,
            'title':  list(movie.title.split('∆')),
            'genre': list(movie.genre.replace(' ','').split(',')),
            'date': movie.date,
            'description': movie.description,
            'poster': movie.poster,
            'frames': list(movie.frames.replace(' ','').split(',')),
            'country':  list(movie.country.split(',')),
            'ifSeries': movie.ifSeries,
            'age': movie.age,
        })

    
    return jsonify(finalJSON), HTTP_200_OK

