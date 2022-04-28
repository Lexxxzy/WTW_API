import difflib
from functools import lru_cache
from flask import Blueprint, jsonify
import pandas as pd
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import User, db
from src.static.seen import Seen

@lru_cache()
def load_recommendations(): 
    movies_matrix = pd.read_csv("src/static/matrix.csv",index_col=0)
    return movies_matrix

movies_matrix = load_recommendations()
recomendations = Blueprint("recomendations", __name__, url_prefix="/api/v1/recomendations")

def check_seen(recommended_movie,watched_movies):
    for movie in watched_movies:
        if difflib.SequenceMatcher(None, recommended_movie, movie).ratio() > 0.82:
            print(movie + '\n\n\n\n')
            return True
    return False

def get_similar_movies(movie_name,user_rating):
    try:
        similar_score = movies_matrix[movie_name]*(user_rating-2.5)
        similar_movies = similar_score.sort_values(ascending=False)
    except:
        similar_movies = pd.Series(dtype=object)
    
    return similar_movies

@recomendations.get('/')
@jwt_required()
def get_recommendations():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    watched_movies = Seen.get(user.favourites, user.likes, user.dislikes)

    print(watched_movies)
    
    similar_movies = pd.DataFrame()

    for movie in watched_movies:
        user_rating = 5
        similar_movies = similar_movies.append(get_similar_movies(movie, user_rating),ignore_index=True)

    all_recommend = similar_movies.sum().sort_values(ascending=False)

    recommended_movies = []
    for movie,score in all_recommend.iteritems():
        if not check_seen(movie,watched_movies):
            recommended_movies.append(movie)    

    if len(recommended_movies) > 100:
        recommended_movies = recommended_movies[0:100]        

    return jsonify({'recomedations' : recommended_movies})
