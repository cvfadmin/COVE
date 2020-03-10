from app import api, db
from app.auth.permissions import AdminOnly
from app.datasets.models import Dataset

from flask import request
from sqlalchemy import asc
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import OwnershipRequest
from .schemas import ownership_requests_schema, ownership_request_schema

"""
Routes to:
- Create ownership request: OwnershipRequestView
- View all ownership requests: AdminAllOwnershipRequestView
- Approve or deny ownership requests: AdminOwnershipRequestView
"""

class OwnershipRequestView(Resource):
    """ Creates ownership requests  """

    @jwt_required
    def post(self, _id):
        """ Anyone who is logged in """

        req_body = request.get_json()
        req_body['dataset'] = _id

        try:
            new = ownership_request_schema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        # TODO: send email?
        # commit all changes
        db.session.add(new)
        db.session.commit()

        return {
            'message': 'Operation Successful',
            'status': 200
        }, 200


class AdminAllOwnershipRequestView(Resource):
    """ View all ownership requests for admins """

    @jwt_required
    def get(self):
        """ Admin Only """

        if not AdminOnly.has_permission(get_jwt_identity()):
            return { 'message': 'Unauthorized user', 'status': 401 }, 401

        requests = OwnershipRequest.query.filter_by(is_resolved=False).order_by(
            asc(OwnershipRequest.date_created)
        ).all() 

        return {
            'num_results': len(requests),
            'results': ownership_requests_schema.dump(requests)
        }, 200


class AdminOwnershipRequestView(Resource):
    """ Approve or deny an ownership request """

    @jwt_required
    def put(self, _id):
        print(request.get_json())
        if not AdminOnly.has_permission(get_jwt_identity()):
            return { 'message': 'Unauthorized user', 'status': 401 }, 401

        is_approved = request.get_json().get('is_approved', None)
        if is_approved is None:
            return {
                'message': 'No "is_approved" attribute in request body',
                'status': 400
            }, 400

        ownership_req = OwnershipRequest.query.filter_by(id=_id).first_or_404()
        if ownership_req.is_resolved:
            return {
                'message': 'Ownership request has already been resolved.',
                'status': 403
            }, 403

        if is_approved:
            # TODO: send email?
            # Transfer ownership
            dataset = Dataset.query.filter_by(id=ownership_req.dataset.id).first()
            dataset.owner = ownership_req.author
        else:
            # TODO: send email?
            db.session.delete(ownership_req)

        # Mark resolved
        ownership_req.is_resolved = True
        # commit all changes
        db.session.commit()

        return {
            'message': 'Operation Successful',
            'status': 200
        }, 200

api.add_resource(OwnershipRequestView, '/datasets/<_id>/ownership-requests')
api.add_resource(AdminAllOwnershipRequestView, '/admin/ownership-requests')
api.add_resource(AdminOwnershipRequestView, '/admin/ownership-requests/<_id>')