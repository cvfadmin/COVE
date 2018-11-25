from app import api, db
from flask import request
from flask_restful import Resource
from app.datasets.models import Dataset, AddDatasetRequest, DeleteDatasetRequest
from app.auth.permissions import AdminOnly
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import CreateDatasetKey, create_key

from .mail import (
    send_dataset_approval,
    send_dataset_denial,
    send_add_ds_request_approval,
    send_add_ds_request_denial,
    send_delete_ds_request_approval,
    send_delete_ds_request_denial,
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
            send_dataset_approval(dataset.contact_email, dataset.id)
        else:
            # send email to author saying it was approved and delete ds
            send_dataset_denial(dataset.contact_email)
            db.session.delete(dataset)

        # commit all changes
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class AdminAddDatasetRequestView(Resource):

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

        add_ds_request = AddDatasetRequest.query.filter_by(id=_id).first_or_404()
        add_ds_request.is_approved = is_approved

        if is_approved:
            # send email to author saying it was approved
            # send link with key
            create_dataset_key = CreateDatasetKey(key=create_key())
            db.session.add(create_dataset_key)

            send_add_ds_request_approval(add_ds_request.email, str(create_dataset_key.key))
        else:
            # send email to author saying it was approved and delete ds
            send_add_ds_request_denial(add_ds_request.email)

        db.session.delete(add_ds_request)
        # commit all changes
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class AdminDeleteDatasetRequestView(Resource):

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

        del_ds_request = DeleteDatasetRequest.query.filter_by(id=_id).first_or_404()
        del_ds_request.is_approved = is_approved

        if is_approved:
            # send email to author saying it was approved
            # send link with key
            dataset = Dataset.query.filter_by(id=del_ds_request.dataset_id).first_or_404()
            db.session.delete(dataset)

            send_delete_ds_request_approval(del_ds_request.email)
        else:
            # send email to author saying it was approved and delete ds
            send_delete_ds_request_denial(del_ds_request.email)

        db.session.delete(del_ds_request)
        # commit all changes
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class CreateDatasetKeyExist(Resource):
    # TODO: Add protections against numerous requests from one IP address
    # Flask-Limiter - https://flask-limiter.readthedocs.io/en/stable/
    def get(self, _key):
        instance = CreateDatasetKey.query.filter_by(key=_key).first()

        if instance is None:
            return {'is_active': False}, 200
        else:
            return {'is_active': True}, 200


api.add_resource(AdminDatasetView, '/admin/datasets/<_id>')
api.add_resource(AdminAddDatasetRequestView, '/admin/requests/add-dataset/<_id>')
api.add_resource(AdminDeleteDatasetRequestView, '/admin/requests/delete-dataset/<_id>')

api.add_resource(CreateDatasetKeyExist, '/admin/create-dataset-key/<_key>')
