from random import randint
from flask import Blueprint, Flask, jsonify, request
from flask_mail import Mail, Message
from src.constants.http_status_codes import HTTP_200_OK
from . import app
verification = Blueprint("verification", __name__, url_prefix="/api/v1/verification")

mail=Mail(app)

otp=randint(000000,999999)

@verification.post('/verify')
def verify():
    email=request.json.get('email', '')
    msg=Message(subject='OTP',sender='wtw.validate@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return jsonify({}), HTTP_200_OK

@verification.post('/validate')
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return "<h3>Email varification succesfull</h3>"
    return "<h3>Please Try Again</h3>"
