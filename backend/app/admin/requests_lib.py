from app import db
from app.datasets.models import Dataset

from flask import request
from flask_restful import Resource
from sqlalchemy import asc


class RequestView(Resource):
    """
    Provides GET and POST functionality for models that inherit Request
    
    GET: Returns all requests associated with a dataset 
    POST: Creates a request in relation to a dataset

    Please Note: Authentication needs to be implemented in child classes
    """
    MultiSchema = None
    SingleSchema = None
    Model = None

    def _get(self, _id):
        # Requests are connected by datasets
        dataset = Dataset.query.filter_by(id=_id).first_or_404()

        requests = self.Model.query.filter_by(dataset=dataset).order_by(
            asc(self.Model.date_created)
        ).all()

        requests_json = self.MultiSchema.dump(requests)

        return {
            'num_results': len(requests),
            'results': requests_json
        }

    def _post(self, _id):
        req_body = request.get_json()
        req_body['dataset'] = _id

        try:
            new = self.SingleSchema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}

        # commit all changes
        db.session.add(new)
        db.session.commit()

        return {
            'message': 'operation successful',
            'new': self.SingleSchema.dump(new),
            'status': 200
        }, 200


class SingleRequestView(Resource):
    """
    Provides PUT functionality for a single model that inherit Request
    
    PUT: Partially updates request model

    Please Note: Authentication needs to be implemented in child classes
    """
    Model = None
    SingleSchema = None

    def _put(self, _id):
        request = self.Model.query.filter_by(id=_id).first_or_404()
        req_body = request.get_json()

        try:
            self.SingleSchema.load(req_body, instance=request, partial=True)
        except ValidationError as err:
            return {'errors': err.messages}

        db.session.query(self.Model).filter_by(id=_id).update(req_body)
        db.session.commit()

        return {
            'message': 'successfully updated',
            'updated': self.SingleSchema.dump(edit_request)
        }


class AllRequestView(Resource):
    """
    Provides GET functionality for all models that inherits Request
    
    GET: Returns list of all request models

    Please Note: Authentication needs to be implemented in child classes
    """
    Model = None
    MultiSchema = None

    def _get(self):

        requests_query = self.Model.query.order_by(
            asc(self.Model.date_created)
        )

        if request.args.get('is_resolved') == 'false':
            requests_query = requests_query.filter_by(is_resolved=False)

        requests_json = self.MultiSchema.dump(requests_query.all())

        return {
            'num_results': len(requests_query.all()),
            'results': requests_json
        }