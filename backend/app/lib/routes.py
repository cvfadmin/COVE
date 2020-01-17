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
    ListSchema = None
    SingleSchema = None

    def get(self):
        model_list = self.Model.query.all()
        model_list_json = self.ListSchema.dump(model_list)
        return {
            'num_results': len(model_list_json),
            'results': model_list_json
        }

    def post(self):
        req_body = request.get_json()
        is_many = request.args.get('many') == 'true'
        schema_to_use = self.ListSchema if is_many else self.SingleSchema

        try:
            new = schema_to_use.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        if is_many:
            for new_model in new:
                db.session.add(new_model)
                db.session.commit()
        else:
            db.session.add(new)
            db.session.commit()

        return {
            'message': 'successfully created',
            'new': schema_to_use.dump(new)
        }
