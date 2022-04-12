from flask import Blueprint
from flask import Blueprint, jsonify
from requests import request
from src.constants.http_errors import *
from src.database import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from .constants.http_status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from .static.favouriteFilms import FavouriteFilm

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


@favourites.put('/<int:id>')
@favourites.patch('/<int:id>')
@jwt_required()
def handle_favourites(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if(user.favourites == None):
        user.favourites = f'{id} '
    else:
        user.favourites += f'{id} '
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
