
from flask_restful import Resource
from .idsearch import SearchById


class FavouriteFilm(Resource):
    def get(favourite):
        if(favourite): 
            fav = favourite.split(' ')
            JsonOfAllFavouritefilms = []
            for x in fav:
                if x != '':
                    JsonOfAllFavouritefilms.append(SearchById.get(x))
            return JsonOfAllFavouritefilms
        else:
            return [{'error' : 'Not found'}]