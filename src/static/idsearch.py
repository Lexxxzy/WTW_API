import requests
from flask_restful import Resource
from .parseFilmToJson import SearchParse
from ..constants.token_api import token


class SearchById(Resource):

    @staticmethod
    def get(filmId, recsId=None,film_name_recs=''):
        url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{filmId}'
        urlFrames = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{filmId}/images?type=STILL&page=1'
        urlSeasons = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{filmId}/seasons'
        urlDistributor = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{filmId}/distributions'
        getall = requests.get(url, headers=token).json()
        getimages = requests.get(urlFrames, headers=token).json()
        getseasons = requests.get(urlSeasons, headers=token).json()
        getdistr = requests.get(urlDistributor, headers=token).json()
        return SearchParse.returnJson(getall, getimages, getseasons, getdistr,recsId,film_name_recs)
