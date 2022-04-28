from flask import Blueprint, request
from flask import Blueprint, jsonify
import requests
from src.constants.http_errors import *
from src.static.searchforrecomendation import searchForRec
from .constants.http_status_codes import HTTP_200_OK
from .static.namesearch import SearchByName
from .constants.token_api import token

"""
    Endpoint /api/v1/search 
    используется для получения информации о фильме по ключевым словам
    Endpoint /api/v1/search/video?id=...
    используется для получения видеоролика связанного с фильмом(трейлер, отрывок)
"""

search = Blueprint("search", __name__, url_prefix="/api/v1/search")

@search.get('/')
def get_search():
    film_name = request.args.get('filmname')

    return jsonify(SearchByName.get(film_name)), HTTP_200_OK

@search.get('/ml')
def get_films_for_ml():
    film_name = request.args.get('filmname')

    return jsonify(searchForRec.get(film_name)), HTTP_200_OK

@search.get('/video')
def get_animated_poster():
    film_id = request.args.get('id')
    urlVideoPoster = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}/videos'
    getvideo = requests.get(urlVideoPoster, headers=token).json()

    return {'video' : getFinalVideo(getvideo)}


def getFinalVideo(getvideo):
    return next(filter(lambda x:
                       x.get('site') == 'YOUTUBE' and (
                           x.get('name').__contains__('Трейлер') or
                           x.get('name').__contains__('Фрагмент') or
                           x.get('name').__contains__('ТВ-ролик')) and
                       ifValidURL(x.get('url')), getvideo.get('items')), None),


def ifValidURL(url):
    r = requests.get(url)  # random video id
    if (("Это видео с ограниченным доступом." in r.text) or
            ("Это видео больше не доступно." in r.text) or
            ("Видео недоступно" in r.text) or
            ('Владелец видео запретил его просмотр в вашей стране.' in r.text) or 
            (url.__contains__('/v/'))):
        return False
    return True