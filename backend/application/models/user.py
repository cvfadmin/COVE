#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from application.models import db, Base
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = sa.Column(sa.String(256), index=True, unique=True)
    password_hash = sa.Column(sa.String(256))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer("cove is good", expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer("cove is good")
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        return data['id']

class Request(Base):
    __tablename__ = 'pending_request'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = sa.Column(sa.String(256), index=True, unique=True)
    firstname = sa.Column(sa.String(64), nullable= True)
    lastname = sa.Column(sa.String(64), nullable= True)
    salt = sa.Column(sa.String(64), nullable = True)

    def __init__(self, email, firstname, lastname):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    def serialize(self):
        return {
                "id": self.id,
                "email": self.email,
                "firstname": self.firstname,
                "lastname": self.lastname
                }
