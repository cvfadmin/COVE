from app import api, db
from flask import request
from flask_restful import Resource
from .schemas import user_schema
from .models import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


class Register(Resource):

    @staticmethod
    def post():
        req_body = request.get_json()
        username, password = req_body.get('username'), req_body.get('password')

        if username is None or password is None:
            return {'error': 'Missing arguments'}
        elif User.query.filter_by(username=username).first() is not None:
            return {'error': 'Username taken'}

        new_user = user_schema.load({
            'username': username,
            'password_hash': User.hash_password(password)
        })

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Created user'}


class Login(Resource):

    @staticmethod
    def post():
        req_body = request.get_json()
        username, password = req_body.get('username'), req_body.get('password')

        if username is None or password is None:
            return {'error': 'Missing arguments'}

        user = User.query.filter_by(username=username).first()

        if user is not None:
            if user.verify_password(password):
                # Generate Token
                access_token = create_access_token(identity=username)
                return {'access_token': access_token}
            else:
                return {'error': 'Credentials provided are incorrect'}
        else:
            return {'error': 'User does not exist'}


class UserView(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'current_user': current_user}


api.add_resource(Register, '/users/register')
api.add_resource(Login, '/users/login')
api.add_resource(UserView, '/users/me')
