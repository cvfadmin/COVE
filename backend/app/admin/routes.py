from app import api, db
from flask import request
from flask_restful import Resource
from sqlalchemy import asc
from app.datasets.models import Dataset
from app.auth.models import User
from app.auth.permissions import AdminOnly, AdminOrDatasetOwner
from .schemas import edit_request_schema, edit_requests_schema, edit_request_message_schema
from .models import EditRequest, EditRequestMessage
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from .mail import (
    send_dataset_approval,
    send_dataset_denial,
    send_edit_request_notification,
    send_admin_message_notification,
    send_owner_message_notification
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

        requests_json = edit_requests_schema.dump(requests).data

        return {
            'num_results': len(requests),
            'results': requests_json
        }

    @jwt_required
    def post(self, _id):

        if not AdminOnly.has_permission(get_jwt_identity()):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        req_body = request.get_json()
        req_body['dataset'] = _id

        try:
            new = edit_request_schema.load(req_body).data
        except ValidationError as err:
            return {'errors': err.messages}

        # send email to owner about new edit request
        send_edit_request_notification(new.dataset.owner.email, new.dataset.name, new.dataset.id)

        # commit all changes
        db.session.add(new)
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class EditRequestSingleView(Resource):

    @jwt_required
    def put(self, _id):

        if not AdminOnly.has_permission(get_jwt_identity()):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        edit_request = EditRequest.query.filter_by(id=_id).first_or_404()
        req_body = request.get_json()

        try:
            edit_request_schema.load(req_body, instance=edit_request, partial=True)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.query(EditRequest).filter_by(id=_id).update(req_body)
        db.session.commit()

        return {
            'message': 'successfully created',
            'updated': edit_request_message_schema.dump(edit_request)
        }



class AdminEditRequestMessageListView(Resource):

    @jwt_required
    def post(self, _id):

        dataset_id = EditRequest.query.filter_by(id=_id).first_or_404().dataset.id
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if not AdminOrDatasetOwner.has_permission(current_user.username, dataset_id):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        req_body = request.get_json()
        req_body['edit_request'] = _id

        if current_user.is_admin:
            req_body['has_admin_read'] = True
        else:
            req_body['has_owner_read'] = True
        try:
            new = edit_request_message_schema.load(req_body).data
        except ValidationError as err:
            return {'errors': err.messages}

        # send email to other party about new message
        if current_user.is_admin:
            # admin sent message - notify owner
            send_owner_message_notification(new.edit_request.dataset.owner.email, new.edit_request.id, dataset_id)
        else:
            send_admin_message_notification(new.edit_request.id, dataset_id)

        # commit all changes
        db.session.add(new)
        db.session.commit()

        return {
            'message': 'operation successful',
            'status': 200
        }, 200


class AdminEditRequestMessageSingleView(Resource):

    @jwt_required
    def put(self, _id):
        message = EditRequestMessage.query.filter_by(id=_id).first_or_404()
        dataset_id = message.edit_request.dataset.id

        if not AdminOrDatasetOwner.has_permission(get_jwt_identity(), dataset_id):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        req_body = request.get_json()
        try:
            edit_request_message_schema.load(req_body, instance=message, partial=True)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.query(EditRequestMessage).filter_by(id=_id).update(req_body)
        db.session.commit()

        return {
            'message': 'successfully created',
            'updated': edit_request_message_schema.dump(message)
        }


class AllEditRequestView(Resource):

    @jwt_required
    def get(self):

        if not AdminOnly.has_permission(get_jwt_identity()):
            return {
                'message': 'Unauthorized user',
                'status': 401
            }, 401

        requests_query = EditRequest.query.order_by(
            asc(EditRequest.date_created)
        )

        if request.args.get('is_resolved') == 'false':
            requests_query = requests_query.filter_by(is_resolved=False)

        requests_json = edit_requests_schema.dump(requests_query.all())[0]

        return {
            'num_results': len(requests_query.all()),
            'results': requests_json
        }


# TODO: Clean up these routes into a better design
api.add_resource(AdminDatasetView, '/admin/datasets/<_id>')
api.add_resource(AdminEditRequestView, '/admin/datasets/<_id>/edit-requests')
api.add_resource(AllEditRequestView, '/admin/edit-requests')
api.add_resource(EditRequestSingleView, '/admin/edit-requests/<_id>')
api.add_resource(AdminEditRequestMessageListView, '/admin/edit-requests/<_id>/messages')
api.add_resource(AdminEditRequestMessageSingleView, '/admin/edit-request-messages/<_id>')
