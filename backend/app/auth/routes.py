from app import api, db
import datetime
from flask import request, current_app
from flask_restful import Resource
from .schemas import user_schema
from .models import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt, jwt_optional
from app.auth.blacklist_helpers import add_token_to_database, revoke_token


class Register(Resource):

    @staticmethod
    def post():
        req_body = request.get_json()
        username, password, email = req_body.get('username'), req_body.get('password'), req_body.get('email')

        if username is None or password is None or email is None:
            return {'error': 'Missing arguments'}
        elif User.query.filter_by(username=username).first() is not None:
            return {'error': 'Username taken'}
        elif User.query.filter_by(email=email).first() is not None:
            return {'error': 'Email is already in use'}

        new_user = user_schema.load({
            'first_name': req_body.get('first_name') if req_body.get('first_name') else None,
            'last_name': req_body.get('last_name') if req_body.get('last_name') else None,
            'username': username,
            'password_hash': User.hash_password(password),
            'email': email
        })

        db.session.add(new_user)
        db.session.commit()

        # Generate Token
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=username, expires_delta=expires)

        # Store the tokens in our database with a status of not currently revoked.
        add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])

        return {
            'access_token': access_token,
            'user_id': new_user.id,
            'permissions': {
                'is_admin': new_user.is_admin
            }
        }


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
                expires = datetime.timedelta(days=1)
                access_token = create_access_token(identity=username, expires_delta=expires)

                # Store the token in our database with a status of not currently revoked.
                add_token_to_database(access_token, current_app.config['JWT_IDENTITY_CLAIM'])

                return {
                    'access_token': access_token,
                    'user_id': user.id,
                    'permissions': {
                        'is_admin': user.is_admin,
                    }
                }
            else:
                return {'error': 'Credentials provided are incorrect'}
        else:
            return {'error': 'User does not exist'}


class UserView(Resource):

    @jwt_required
    def get(self):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        return {'result': user_schema.dump(current_user)}


class UserLogoutView(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        user_identity = get_jwt_identity()
        revoke_token(jti, user_identity)
        return {"message": "Successfully logged out"}, 200


api.add_resource(Register, '/users/register')
api.add_resource(Login, '/users/login')
api.add_resource(UserLogoutView, '/users/logout')
api.add_resource(UserView, '/users/me')
