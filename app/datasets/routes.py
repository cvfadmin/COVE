from app import api, db
from flask import request
from flask_restful import Resource
from .models import Dataset
from .schemas import dataset_schema, add_dataset_request_schema


class SingleDatasetView(Resource):

    def get(self, d_id):
        dataset = Dataset.query.filter_by(id=d_id).first()
        ds_json = dataset_schema.dump(dataset)
        return {'dataset': ds_json}


class AddDatasetRequestView(Resource):

    def post(self):
        req_body = request.get_json()
        new_request = add_dataset_request_schema.load(req_body)

        db.session.add(new_request)
        db.session.commit()

        return {'message': 'Request recorded'}

    def put(self):
        req_body = request.get_json()
        pass



api.add_resource(SingleDatasetView, '/datasets/<d_id>')
api.add_resource(AddDatasetRequestView, '/requests/datasets/new')