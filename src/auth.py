from datetime import timedelta
import os
from flask import Blueprint, request, jsonify, send_from_directory
import werkzeug
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.constants.http_errors import *
from src.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_408_REQUEST_TIMEOUT, HTTP_409_CONFLICT
import uuid as uuid

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), 'data')


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
        'avatar': user.avatar_URL,
        'favourites': 0 if user.favourites is None else len(''.join(user.favourites).split(' '))-1,
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
@jwt_required()
def set_avatar():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    imagefile = request.files['image']
    file_name = werkzeug.utils.secure_filename(imagefile.filename)
    image_name = str(uuid.uuid1()) + '_' + file_name

    if not imagefile:
        return jsonify({'error': 'Bad upload!'}), HTTP_400_BAD_REQUEST

    #save new avatar
    imagefile.save(os.path.join('src/files', image_name))

    #delete previous avatar
    os.remove(os.path.join('src/files/', f'{user.avatar_URL}'))

    #set and commit new avatar url to database
    user.avatar_URL = image_name
    db.session.commit()

    imagefile.close

    return jsonify({}), HTTP_200_OK


@auth.route('/files/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory('files', filename, as_attachment=True)
