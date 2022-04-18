import os
from src.suggestions import suggestions
from flask_jwt_extended import JWTManager
from src.favourites import favourites
from datetime import timedelta
from src.search import search
from src.likes import likes
from flask_mail import Mail
from src.auth import auth
from flask import (
    Flask,
    render_template,
    request,
    Blueprint,
    jsonify,
)
from flask_mail import (
    Mail,
    Message
)
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from src.database import (
    User, 
    db
)



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCKEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            MEDIA_FOLDER = os.environ.get("MEDIA_FOLDER"),
        )
    else:
        app.config.from_mapping(test_config)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=90)
    
    app.config.from_pyfile('mailconfig.cfg')

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(favourites)
    app.register_blueprint(suggestions)
    app.register_blueprint(likes)
    app.register_blueprint(search)
    
    verification = Blueprint("verification", __name__, url_prefix="/api/v1/verification")

    mail=Mail(app)
    
    @verification.post('/verify')
    def verify():
        
        email=request.json.get('email', '')
        user = User.query.filter_by(email=email).first()
        msg=Message(subject='What to watch',sender='wtw.validate@gmail.com',recipients=[email])
        msg.html = render_template('email.html', otp = str(user.code), email = email)
        mail.send(msg)
        return jsonify({}), HTTP_200_OK

    @verification.post('/validate')
    def validate():
        email=request.json.get('email', '')
        otp=request.json.get('code', '')
        user = User.query.filter_by(email=email).first()
        if user.code==int(otp):
            user.code = None
            user.isAcivated = 'true'
            db.session.commit()
            return {'success' : '200'}, HTTP_200_OK
        return  {'error' : 'Wrong code!'}, HTTP_400_BAD_REQUEST

    app.register_blueprint(verification)

    return app

