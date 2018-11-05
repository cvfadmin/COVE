from app import db
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError


class SingleResourceByIdView(Resource):
    Model = None
    Schema = None

    def get(self, _id):
        model_instance = self.Model.query.filter_by(id=_id).first_or_404()
        model_json = self.Schema.dump(model_instance)
        return {'result': model_json}


class ListResourceView(Resource):
    Model = None
    Schema = None

    def get(self):
        model_list = self.Model.query.all()
        model_list_json = self.Schema.dump(model_list)
        return {'results': model_list_json}

    def post(self):
        req_body = request.get_json()

        try:
            new_model = self.Schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.add(new_model)
        db.session.commit()

        return {'message': 'Object created successfully'}