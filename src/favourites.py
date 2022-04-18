from flask import Blueprint
from flask import Blueprint, jsonify
from src.constants.http_errors import *
from src.database import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from .constants.http_status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from .static.favouriteFilms import FavouriteFilm

""" 
    Endpoint /api/v1/favourites/... используется для получения
    информации о любимых фильмах и сериалах, а также ее добавления
    для конкретного юзера

    - / получение json с информацией о фильмах
    - /is-favourite/<int:id> проверка на то является ли фильм любимым
    - /<int:id> добавление фильма в любимые
"""

favourites = Blueprint("favourites", __name__, url_prefix="/api/v1/favourites")


@favourites.get('/')
@jwt_required()
def get_favourites():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    all_user_favourites = FavouriteFilm.get(user.favourites)
    return {"favourites":
            all_user_favourites,
            }, HTTP_200_OK


@favourites.get('/is-favourite/<int:id>')
@jwt_required()
def is_favourite(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    is_favourite = False

    if(user.favourites != None):
        fav_list = user.favourites.split(' ')
        is_favourite = f'{id}' in fav_list

    return {"isFavourite":
            is_favourite,
            }, HTTP_200_OK


@favourites.put('/<int:id>')
@favourites.patch('/<int:id>')
@jwt_required()
def handle_favourites(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if(user.favourites == None):
        user.favourites = f'{id} '
        db.session.commit()
        return jsonify({}), HTTP_204_NO_CONTENT

    fav_list = user.favourites.split(' ')

    if(f'{id}' in fav_list):
        fav_list.remove(f'{id}')
        user.favourites = None if len(fav_list) < 2 else " ".join(fav_list)
    else:
        user.favourites += f'{id} '

    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
