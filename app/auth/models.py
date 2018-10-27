from passlib.apps import custom_app_context as pwd_context
from app import db
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def __repr__(self):
        return '<User(username={self.username!r})>'.format(self=self)