from flask_mail import Message
from app import api, db, mail
from flask import request
from flask_restful import Resource

class Email(Resource):

    @staticmethod
    def post():
        req_body = request.get_json()
        msg = Message()

        # TO DO:
        # Add username and password for message

        msg.subject = req_body.get('subject')
        msg.sender = req_body.get('sender')
        msg.recipients = req_body.get('recipients')
        msg.body = req_body.get('message')

        mail.sender(msg)
        return {'message': 'Sent Email'}


api.add_resource(Email, '/admin/email')
