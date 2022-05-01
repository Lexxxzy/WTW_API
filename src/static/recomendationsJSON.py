import requests
from flask_restful import Resource
from ..constants.token_api import token
from .idsearch import SearchById
from src.database import db


class RecomendationsJSON(Resource):
    
    @staticmethod
    def get(films, user):
      listWithRecomendations = []
      i=0
      for k in range(0,len(films) -1):
        url_get_name = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={films[k]}&page=1'
        id_to_name = requests.get(url_get_name, headers=token).json().get('films')
        if(len(id_to_name) != 0):
          if(id_to_name is not None or len(id_to_name)>0):
            film_id = id_to_name[0]['filmId']
            listWithRecomendations.append(SearchById.get(film_id,i,films[k]))
            i+=1
        else:
          rec_list = user.recomendations.split('~')

          if(films[k] in rec_list):
              rec_list.remove(films[k])
              user.recomendations = None if len(rec_list) < 2 else "~".join(rec_list)

          db.session.commit()

      return listWithRecomendations
     
    