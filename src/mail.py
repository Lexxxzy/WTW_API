from flask_mail import Mail
from flask import (
    render_template,
    request,
    Blueprint,
    jsonify,
)
from flask_mail import (
    Mail,
    Message
)
from src import mail
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from src.database import (
    User, 
    db
)

verification = Blueprint("verification", __name__, url_prefix="/api/v1/verification")

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
