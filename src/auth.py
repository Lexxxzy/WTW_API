from datetime import timedelta
import os
from flask import Blueprint, request, jsonify
import werkzeug
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.constants.http_errors import *
from src.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(username) < 3:
        return jsonify({'error': SIGN_UP_USERNAME_SHORT}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': SIGN_UP_USER}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': SIGN_UP_EMAIL_VALID}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': SIGN_UP_EMAIL_EXISTS}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': SIGN_UP_USERNAME_EXISTS}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
        }
    }), HTTP_201_CREATED


@auth.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_password_correct = check_password_hash(user.password, password)

        if is_password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            accesTokenExpiresIn = 90 * 24 * 60 * 60

            return jsonify({
                'idToken': access,
                'expiresIn': accesTokenExpiresIn,
                'username': user.username,
                'email': user.email
            }), HTTP_200_OK
        else:
            return jsonify({'error': SIGN_IN_PASSWORD}), HTTP_200_OK

    else:
        return jsonify({'error': SIGN_IN_EMAIL}), HTTP_200_OK


@auth.get("/user")
@jwt_required()
def user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email,
        'favourites': 0 if user.favourites is None else len(''.join(user.favourites).split(' ')),
        'likes': 0 if user.likes is None else len(''.join(user.likes).replace(' ', '').split(',')),
        'dislikes': 0 if user.dislikes is None else len(''.join(user.dislikes).replace(' ', '').split(',')),
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK


@auth.post("/setavatar")
#@jwt_required()
def set_avatar():
    # user_id = get_jwt_identity()
    # user = User.query.filter_by(id=user_id).first()

    imagefile = request.files['image']
    imagefile.save(os.path.join('src/files',werkzeug.utils.secure_filename(imagefile.filename)))
    imagefile.close

#user.avatar_URL = './files/avatars/' + filename

    return jsonify({}), HTTP_200_OK
