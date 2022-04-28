import requests
from googletrans import Translator
from flask_restful import Resource
from ..constants.token_api import token


class searchForRec(Resource):
    @staticmethod
    def get(film_name):
        urlWithFilmId = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={film_name}&page=1'
        resultFilm = requests.get(urlWithFilmId, headers=token).json()
        filmId = (list(map(lambda x: x.get('filmId'), resultFilm.get('films')))[0:1])[0]
        translator = Translator()
        url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{filmId}'
        urlActorAndDirector = f'https://kinopoiskapiunofficial.tech/api/v1/staff?filmId={filmId}'
        getActorAndDirector = requests.get(urlActorAndDirector, headers=token).json()
        getall = requests.get(url, headers=token).json()
        
        resultJsonFile = {
            'type' : getall.get('type'),
            'title': getall.get('nameOriginal'),
            'director' : list(map(lambda x: x.get('nameEn'),filter(lambda x: x.get('professionKey')=='DIRECTOR',getActorAndDirector[0:40]))),
            'cast' : list(map(lambda x: x.get('nameEn'),filter(lambda x: x.get('professionKey')=='ACTOR',getActorAndDirector[0:40]))),
            'country': list(map(lambda x: translator.translate(x.get('country'), dest='en').text, getall.get('countries'))),
            'date': getall.get('year'),
            'genre': (list(map(lambda x: translator.translate(x.get('genre'), dest='en').text, getall.get('genres')))),
            'description': translator.translate(getall.get('description'), dest='en').text,
        }
       
        return resultJsonFile