import difflib
from functools import lru_cache
from flask import Blueprint, jsonify
import pandas as pd
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.constants.http_status_codes import HTTP_204_NO_CONTENT
from src.database import User, db
from src.static.getSimilarAPI import SimilarMoviesYandex
from src.static.recomendationsJSON import RecomendationsJSON
from src.static.seen import Seen


@lru_cache()
def load_recommendations():
    movies_matrix = pd.read_csv("src/static/matrix.csv", index_col=0)
    return movies_matrix


movies_matrix = load_recommendations()
recomendations = Blueprint("recomendations", __name__,
                           url_prefix="/api/v1/recomendations")
yandex_rec = []


def check_seen(recommended_movie, watched_movies):
    for movie in watched_movies:
        if difflib.SequenceMatcher(None, recommended_movie, movie).ratio() > 0.82:
            return True
    return False


def get_similar_movies(movie_name, user_rating):
    try:
        similar_score = movies_matrix[movie_name]*(user_rating-2.5)
        similar_movies = similar_score.sort_values(ascending=False)[0:20]
        return similar_movies
    except:
        yandex_rec.extend((SimilarMoviesYandex.get(movie_name)))


@recomendations.get('/')
@jwt_required()
def get_recommendations():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if (user.favourites is not None or user.likes is not None):
        if (user.recomendations == None or len(user.recomendations) == 0):
            watched_movies = Seen.get(
                user.favourites, user.likes, user.dislikes)
            liked_movies = Seen.get_liked(user.favourites, user.likes)

            similar_movies = pd.DataFrame()
            for movie in liked_movies:
                user_rating = 5
                similar_movies = similar_movies.append(
                    get_similar_movies(movie, user_rating), ignore_index=True)
            all_recommend = similar_movies.sum().sort_values(ascending=False)
            recommended_movies = []

            for movie, score in all_recommend.iteritems():
                if not check_seen(movie, watched_movies):
                    recommended_movies.append(movie)

            for movie in yandex_rec:
                if not check_seen(movie, watched_movies):
                    recommended_movies.append(movie)

            if len(recommended_movies) > 100:
                recommended_movies = recommended_movies[0:100]

            user.recomendations = '~'.join(map(str, recommended_movies))
            db.session.commit()

            return jsonify({'recomendations': RecomendationsJSON.get(recommended_movies[0:20],user)})
        else:
            recomendations_from_db = user.recomendations
            recomendations_list = recomendations_from_db.split('~')
            return jsonify({'recomendations': RecomendationsJSON.get(recomendations_list[:19],user)})
    else:
        return jsonify({'recomendations': []})


@recomendations.put('/<title>')
@recomendations.patch('/<title>')
@jwt_required()
def delete_from_recomendations(title):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    rec_list = user.recomendations.split('~')

    if(title in rec_list):
        rec_list.remove(title)
        user.recomendations = None if len(rec_list) < 2 else "~".join(rec_list)

    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
