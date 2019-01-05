from app import api, db
from flask import request
from flask_restful import Resource
from sqlalchemy import asc
from app.datasets.models import Dataset
from app.auth.permissions import AdminOnly, AdminOrDatasetOwner
from .schemas import edit_request_schema, edit_requests_schema, edit_request_message_schema
from .models import EditRequest
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from .mail import (
    send_dataset_approval,
    send_dataset_denial,
)


class AdminDatasetView(Resource):

    @jwt_required
    def put(self, _id):

        if not AdminOnly.has_permission(get_jwt_identity()):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        is_approved = request.get_json().get('is_approved', None)
        if is_approved is None:
            return {
                'message': 'No "is_approved" attribute in request body',
                'status': 400
            }, 400

        dataset = Dataset.query.filter_by(id=_id).first_or_404()
        if dataset.is_approved:
            return {
                'message': 'Dataset has already been approved.',
                'status': 403
            }, 403
        dataset.is_approved = is_approved

        if is_approved:
            # send email to author saying it was approved
            send_dataset_approval(dataset.owner.email, dataset.id)
        else:
            # send email to author saying it was approved and delete ds
            send_dataset_denial(dataset.owner.email)
            db.session.delete(dataset)

        # commit all changes
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class AdminEditRequestView(Resource):

    @jwt_required
    def get(self, _id):

        if not AdminOrDatasetOwner.has_permission(get_jwt_identity(), _id):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        dataset = Dataset.query.filter_by(id=_id).first_or_404()

        requests = EditRequest.query.filter_by(dataset=dataset).order_by(
            asc(EditRequest.date_created)
        ).all()

        requests_json = edit_requests_schema.dump(requests)

        return {
            'num_results': len(requests),
            'results': requests_json
        }

    @jwt_required
    def post(self, _id):

        if not AdminOrDatasetOwner.has_permission(get_jwt_identity(), _id):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        req_body = request.get_json()
        req_body['dataset'] = _id

        try:
            new = edit_request_schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        # commit all changes
        db.session.add(new)
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class AdminEditRequestMessageView(Resource):

    @jwt_required
    def post(self, _id):

        dataset_id = EditRequest.query.filter_by(id=_id).first_or_404().dataset.id
        if not AdminOrDatasetOwner.has_permission(get_jwt_identity(), dataset_id):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        req_body = request.get_json()
        req_body['edit_request'] = _id

        try:
            new = edit_request_message_schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        # commit all changes
        db.session.add(new)
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


api.add_resource(AdminDatasetView, '/admin/datasets/<_id>')
api.add_resource(AdminEditRequestView, '/admin/datasets/<_id>/edit-requests')
api.add_resource(AdminEditRequestMessageView, '/admin/edit-requests/<_id>/messages')
