#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from application.models import db, Base
from sqlalchemy.ext.declarative import AbstractConcreteBase
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

class Request(AbstractConcreteBase, Base):
    id = sa.Column(sa.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = sa.Column(sa.String(256), index=True)
    firstname = sa.Column(sa.String(64), nullable= True)
    lastname = sa.Column(sa.String(64), nullable= True)
    dataset_name = sa.Column(sa.String(1000), nullable=False)
    salt = sa.Column(sa.String(64), nullable = True)



class AddRequest(Request):
    __tablename__ = 'add_request'
    year = sa.Column(sa.Integer, nullable= False)
    intro = sa.Column(sa.Text, nullable=False)
    url = sa.Column(sa.String(1000), nullable=False)
    __mapper_args__ = {
                'polymorphic_identity': 'add',
                'concrete': True
    }
    def __init__(self, firstname="",lastname="", email="", dataset_name="", year=9999, intro="", url=""):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.dataset_name = dataset_name
        self.year = year
        self.intro = intro
        self.url = url

    def serialize(self):
        return {
                "id": self.id,
                "email": self.email,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "dataset_name": self.dataset_name,
                "year":self.year,
                "intro" : self.intro,
                "url" : self.url
                }

class EditRequest(Request):
    __tablename__ = 'edit_request'
    target_id = sa.Column(sa.Integer, nullable = False)
    __mapper_args__ = {
                'polymorphic_identity': 'edit',
                'concrete': True
    }
    def __init__(self, firstname="",lastname="", email="", target_id = None, dataset_name=""):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.dataset_name = dataset_name    
        self.target_id = target_id
        self.dataset_name = dataset_name

    def serialize(self):
        return {
                "id": self.id,
                "email": self.email,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "dataset_id" : self.target_id,
                "dataset_name": self.dataset_name
                }

class DeleteRequest(Request):
    __tablename__ = 'delete_request'
    target_id = sa.Column(sa.Integer, nullable = False)
    reason = sa.Column(sa.Text, nullable=False)
    __mapper_args__ = {
                'polymorphic_identity': 'delete',
                'concrete': True
    }
    def __init__(self, firstname="",lastname="", email="", target_id = None, dataset_name="", reason=""):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.dataset_name = dataset_name    
        self.target_id = target_id
        self.dataset_name = dataset_name
        self.reason = reason

    def serialize(self):
        return {
                "id": self.id,
                "email": self.email,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "dataset_id": self.target_id,
                "dataset_name" : self.dataset_name,
                "reason" : self.reason
                }
