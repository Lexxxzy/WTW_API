
from flask import jsonify
from src.constants.http_status_codes import HTTP_200_OK
from src.database import ComingSoon

def get_final_json(key_word):
  
    coming_soon = ComingSoon.query.all()
    finalJSON = []

    for movie in coming_soon:
        if (movie.tags.__contains__(key_word)):
            finalJSON.append({
                'id': movie.id,
                'title':  list(movie.title.split('∆')),
                'genre': list(movie.genre.replace(' ','').split(',')),
                'date': movie.date,
                'description': movie.description,
                'poster': movie.poster,
                'frames': list(movie.frames.replace(' ','').split(',')),
                'country':  list(movie.country.split(',')),
                'ifSeries': movie.ifSeries,
                'age': movie.age,
                'ratingKinopoisk' : float(movie.ratingKinopoisk) if movie.ratingKinopoisk!=None else movie.ratingKinopoisk,
                'ratingIMDb' : float(movie.ratingIMDb) if movie.ratingIMDb!=None else movie.ratingIMDb,
            })

    
    return jsonify(finalJSON)