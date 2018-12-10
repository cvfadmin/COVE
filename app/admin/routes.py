from app import api, db
from flask import request
from flask_restful import Resource
from app.datasets.models import Dataset
from app.auth.permissions import AdminOnly
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
        dataset.is_approved = is_approved\

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


api.add_resource(AdminDatasetView, '/admin/datasets/<_id>')
