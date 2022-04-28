from flask_restful import Resource
import requests
from sqlalchemy import all_
from .idsearch import SearchById
from ..constants.token_api import token

class Seen(Resource):
    def get(favourites, liked, disliked):
        seen_favs = favourites.split(' ') if favourites else []
        seen_likes = liked.split(' ') if liked else ['462360', '437410']
        seen_dis = disliked.split(' ') if disliked else []
        all_seen = seen_favs + seen_likes + seen_dis
        if(len(all_seen) > 0): 
            seen_films_titles = []
            for film_id in all_seen:
                if film_id != '':
                    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}'
                    all_info = requests.get(url, headers=token).json()
                    year = all_info.get('year')
                    name = all_info.get('nameOriginal')+ f' ({year})'
                    seen_films_titles.append(name)
            return seen_films_titles
        else:
            return []