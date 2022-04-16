import requests
from flask_restful import Resource
from ..constants.token_api import token
from .idsearch import SearchById


class SearchByName(Resource):
    
    @staticmethod
    def get (film_name):
        url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={film_name}&page=1'
        result = requests.get(url, headers=token).json()
        listWithIdFilms = list(map(lambda x: x.get('filmId'), result.get('films')))[0:5]   
        listWithFilms = []
        for x in listWithIdFilms:
            listWithFilms.append(SearchById.get(x))
        return listWithFilms
    