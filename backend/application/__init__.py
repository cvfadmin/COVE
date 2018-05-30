#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.cors import CORS

from application.models import db
from application.views import mail
from application.views.api import api

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(api, resources={r"/api/*": {"origins": "*"}})


app.config.from_object(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://johndickinson:@localhost/test3"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cove:password@localhost:5432/postgres"

app.config["SECRET_KEY"] = "cove is good"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'coveproj1@gmail.com'
app.config["MAIL_PASSWORD"] = 'coveadmin1'
mail.init_app(app)

db.init_app(app)

app.register_blueprint(api)
