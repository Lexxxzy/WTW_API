from flask import Blueprint, request
from flask import Blueprint, jsonify
from src.constants.http_errors import *
from .constants.http_status_codes import HTTP_200_OK
from .static.namesearch import SearchByName

"""
    Endpoint /api/v1/search... 
    используется для получения информации о фильме по ключевым словам
"""

search = Blueprint("search", __name__, url_prefix="/api/v1/search")


@search.get('/')
def get_search():
    film_name = request.args.get('filmname')

    return jsonify(SearchByName.get(film_name)), HTTP_200_OK