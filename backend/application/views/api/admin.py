from flask.views import MethodView
from flask import request, jsonify, g, abort
from flask.ext.mail import Message 
from datetime import datetime
from application.views import mail
from application.models import db
from application.models.user import User, Request
from application.utils.dbmanage.model_insert import ModelInsert
from application.utils.dbmanage.model_query import ModelQuery
from flask_httpauth import HTTPBasicAuth
import hashlib, uuid
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user_id = User.verify_auth_token(username_or_token)
    user = db.session.query(User).filter_by(id = user_id).first()
    if not user:
        # try to authenticate with username/password
        user = db.session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

def verify_email(mail, hashed_str):
    usr = db.session.query(Request).filter_by(email=mail).first()
    if not usr:
        return False
    else:
        if usr.salt is None:
            return False
        else:
            m = hashlib.new('sha512')
            m.update(usr.salt + mail)
            url_suffix = m.hexdigest()
            if url_suffix != hashed_str:
                return False
            else:
                return True

class ProcessRequest(MethodView):
    def post(self):
        email = request.json.get('email')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        ModelInsert.insertRequest(email, firstname, lastname, db.session)
        db.session.commit()
        return jsonify({"message":'Request sent, we\'ll send a link to your email.'}), 200

    @auth.login_required
    def put(self, request_id):
        rqst = db.session.query(Request).filter_by(id=request_id).first()
        if rqst is not None and rqst.salt is None:
            salt = uuid.uuid4().hex
            rqst.salt = salt
            m = hashlib.new('sha512')
            m.update(salt + rqst.email)
            url_suffix = m.hexdigest()
            url = "localhost:8000/#/new_dataset/" + url_suffix
            subject = "Invitation from COVE" 
            message = "You can use the following link to submit your dataset to COVE: \n" + url
            msg = Message(subject, sender="coveproj@gmail.com", recipients=[rqst.email])
            print "message sent"
            msg.body = message
            mail.send(msg)
        db.session.commit()
        return jsonify({"message":"Invitation sent!"}), 200

class New_dataset(MethodView):
    def get(self):
        mail = request.args.get("email")
        hashed_str = request.args.get("suffix")
        flag = verify_email(mail, hashed_str)
        if flag:
            return jsonify({"message":"Authorized"}), 200
        else:
            return jsonify({"error":"Not Authorized"}), 401

    def post(self):
        mail = request.json.get('email')
        hashed_str = request.json.get('suffix')
        flag = verify_email(mail, hashed_str)
        if not flag:
            return jsonify({"error":"Not Authorized"}), 401  
        dst = ModelQuery.getDatasetByName(request.json.get('name'), db.session())
        if dst:
            return jsonify({"error":"Dataset name confliction"}), 401
        year = request.json.get('year');
        size = request.json.get('size');
        if not year:
            year = 0
        if not size:
            size = 0
        dst = ModelInsert.insertDataset(
                request.json.get('name'), \
                request.json.get('url'), \
                request.json.get('description'), \
                "",\
                False,\
                request.json.get('author'),\
                year,\
                size,\
                "",\
                "",\
                "",\
                request.json.get('paper'), \
                request.json.get('conferences'), \
                request.json.get('tasks').split(';'),\
                request.json.get('datatypes').split(';'), \
                "", \
                request.json.get('annotations').split(';'), \
                request.json.get('thumbnails').split(';'), \
                request.json.get('institutions').split(';'),\
                db.session)
        if dst:
            db.session.commit()
            return jsonify({"message":"Succeed"}), 200
        else:
            return jsonify({"error":"Not Valid"}), 401


class Administration(MethodView):
    @auth.login_required
    def get(self):
        value = []
        pendings = db.session.query(Request).filter_by(salt=None).all();
        for rqst in pendings:
            value.append(rqst.serialize())
        response = jsonify(pending_requests=value)
        response.status_code = 200 
        return response

    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        message = []
        if verify_password(username, password):
            token = g.user.generate_auth_token(600)
            return jsonify({'token': token.decode('ascii'), 'duration': 600})
        else:
            message.append({"message":"Password is incorrect for the specified username"})
            dic={
                "errors":message
            }
            return jsonify(dic),422

