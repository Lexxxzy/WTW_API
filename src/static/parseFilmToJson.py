import requests


class SearchParse:

    @staticmethod
    def returnJson(getall, getimages, getseasons, getdistr):
        if getall.get('ratingAgeLimits') is None:
            age = None
        else:
            age = int(getall.get('ratingAgeLimits').replace('age', ''))
        resultJsonFile = {
            'id': getall.get('kinopoiskId'),
            'title': [getall.get('nameRu'), getall.get('nameOriginal')],
            'genre': (list(map(lambda x: x.get('genre'), getall.get('genres')))),
            'ratingKinopoisk': getall.get('ratingKinopoisk'),
            'ratingIMDb': getall.get('ratingImdb'),
            'date': getall.get('year'),
            'description': getall.get('description'),
            'poster': getall.get('posterUrl'),
            'frames': list(map(lambda x: x.get('previewUrl'), getimages.get('items')))[0:5],
            'country': list(map(lambda x: x.get('country'), getall.get('countries'))),
            'ifSeries': getall.get('serial'),
            'seasons': getseasons.get('total'),
            'dateTo': getall.get('endYear'),
            'age': age,
            'studio': list(set(map(lambda x: x[0]['name'], filter(None, (map(lambda x: x.get('companies'), getdistr.get('items'))))))),
            'video': '',
        }
        return resultJsonFile


