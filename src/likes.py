from flask import Blueprint
from flask import Blueprint, jsonify
from requests import request
from src.constants.http_errors import *
from src.database import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from .constants.http_status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from .static.favouriteFilms import FavouriteFilm

likes = Blueprint("likes", __name__, url_prefix="/api/v1/likes")


@likes.get('/')
@jwt_required()
def get_likes():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    all_user_likes = FavouriteFilm.get(user.likes)
    return {"Likes":
            all_user_likes,
            }, HTTP_200_OK


@likes.get('/is-liked/<int:id>')
@jwt_required()
def is_liked(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    is_liked = False

    if(user.likes != None):
       fav_list = user.likes.split(' ')
       is_liked = f'{id}' in fav_list

    return {"isLiked":
            is_liked,
            }, HTTP_200_OK


@likes.put('/<int:id>')
@likes.patch('/<int:id>')
@jwt_required()
def handle_likes(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if(user.likes == None):
        user.likes = f'{id} '
        db.session.commit()
        return jsonify({}), HTTP_204_NO_CONTENT

    likes_list = user.likes.split(' ')

    if(f'{id}' in likes_list):
        likes_list.remove(f'{id}')
        user.likes = None if len(likes_list)<2 else " ".join(likes_list)
    else:
        user.likes += f'{id} '

    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT

@likes.put('/dislikes/<int:id>')
@likes.patch('/dislikes/<int:id>')
@jwt_required()
def handle_dislikes(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if(user.dislikes == None):
        user.dislikes = f'{id} '
        db.session.commit()
        return jsonify({}), HTTP_204_NO_CONTENT

    dislikes_list = user.dislikes.split(' ')

    if(f'{id}' in dislikes_list):
        dislikes_list.remove(f'{id}')
        user.dislikes = None if len(dislikes_list)<2 else " ".join(dislikes_list)
    else:
        user.dislikes += f'{id} '

    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT