from app import api, db
from flask import request
from flask_restful import Resource
from .models import Dataset, AddDatasetRequest
from marshmallow import ValidationError

from .schemas import (
    dataset_schema,
    add_dataset_request_schema,
    delete_dataset_request_schema,
    add_dataset_request_list_schema,
    delete_dataset_request_list_schema,
    dataset_list_schema,
)


class DatasetByIdView(Resource):

    def get(self, d_id):
        dataset = Dataset.query.filter_by(id=d_id).first()
        ds_json = dataset_schema.dump(dataset)
        return {'dataset': ds_json}


class DatasetView(Resource):

    def get(self):
        # TODO: Add search functionality here
        datasets = Dataset.query.all()
        ds_json = dataset_list_schema.dump(datasets)
        return {'datasets': ds_json}

    def post(self):
        req_body = request.get_json()

        try:
            new_dataset = dataset_schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.add(new_dataset)
        db.session.commit()

        return {'message': 'Created Dataset'}


class AddDatasetRequestView(Resource):

    def get(self):
        requests = AddDatasetRequest.query.all()
        reqs_json = add_dataset_request_list_schema.dump(requests)
        return {'add_requests': reqs_json}

    def post(self):
        req_body = request.get_json()

        try:
            new_request = add_dataset_request_schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.add(new_request)
        db.session.commit()

        return {'message': 'Request recorded'}


class DeleteDatasetRequestView(Resource):

    def get(self):
        requests = AddDatasetRequest.query.all()
        reqs_json = delete_dataset_request_list_schema.dump(requests)
        return {'delete_requests': reqs_json}

    def post(self):
        req_body = request.get_json()

        try:
            new_request = delete_dataset_request_schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.add(new_request)
        db.session.commit()

        return {'message': 'Request recorded'}


api.add_resource(DatasetView, '/datasets/')
api.add_resource(DatasetByIdView, '/datasets/<d_id>')
api.add_resource(AddDatasetRequestView, '/requests/datasets/add')
api.add_resource(DeleteDatasetRequestView, '/requests/datasets/delete')