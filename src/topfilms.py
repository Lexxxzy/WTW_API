from flask import Blueprint
from flask import Blueprint, jsonify
from src.constants.http_errors import *
from .constants.http_status_codes import HTTP_200_OK
from .static.topFilms import TopFilm

top_films = Blueprint("top_films", __name__, url_prefix="/api/v1/top-films")


@top_films.get('/')
def get_topfilms():

    return jsonify(TopFilm.get()), HTTP_200_OK
