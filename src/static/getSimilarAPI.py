import requests
from flask_restful import Resource
from ..constants.token_api import token
from .idsearch import SearchById


class SimilarMoviesYandex(Resource):
    
    @staticmethod
    def get(film_name):
        url_get_name = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={film_name}&page=1'
        id_to_name = requests.get(url_get_name, headers=token).json().get('films')
        film_id = id_to_name[0]['filmId']
        film_year = id_to_name[0]['year']

        url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}/similars'
        result = requests.get(url, headers=token).json()
        listWithNameFilms = list(map(lambda x: x.get('nameEn') + f' ({film_year})', filter(lambda x: x.get('nameEn')!=None , result.get('items'))))
        
        return listWithNameFilms