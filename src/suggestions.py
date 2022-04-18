from signal import Sigmasks
from flask import Blueprint
from flask import Blueprint, jsonify
from src.constants.http_errors import *
from src.database import ComingSoon
from src.static.finalJSON import get_final_json
from .constants.http_status_codes import HTTP_200_OK
from .static.topFilms import TopFilm

"""
    Endpoint /api/v1/suggestions... 
    предоставляет доступ до рекомендаций (топа фильмов)
    по конкретным запросам:
    - топ ожидаемых фильмов /upcoming
    - топ Netflix /netflix
    - топ Marvel /marvel
    - популярные фильмы /top-films
"""

suggestions = Blueprint("suggestions", __name__, url_prefix="/api/v1/suggestions")


@suggestions.get('/upcoming')
def get_trending():
    return get_final_json('coming_soon'), HTTP_200_OK

@suggestions.get('/netflix')
def get_netflix():
    return get_final_json('top10_netflix'), HTTP_200_OK

@suggestions.get('/marvel')
def get_marvel():
    return get_final_json('top10_marvel'), HTTP_200_OK

@suggestions.get('/top-films')
def get_topfilms():
    return jsonify(TopFilm.get()), HTTP_200_OK