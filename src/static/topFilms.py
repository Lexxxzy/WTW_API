import requests
from flask_restful import Resource
from ..constants.token_api import token
from .idsearch import SearchById


class TopFilm(Resource):
    
    @staticmethod
    def get():
        url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page=1'
        result = list(map(lambda x:x.get('filmId'),list(requests.get(url, headers=token).json().get('films'))[8:11]))
        
        listWithFilms = []
        for x in result:
            listWithFilms.append(SearchById.get(x))
        return listWithFilms
   