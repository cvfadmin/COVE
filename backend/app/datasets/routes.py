from app import api, db
from config import Config
from flask import request
from marshmallow import ValidationError
from app.lib.routes import SingleResourceByIdView, ListResourceView
from app.auth.models import User
from .models import Dataset, Tag
from app.auth.permissions import AdminOnly
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from .filter import dataset_tag_filter
from app.admin.mail import send_dataset_to_approve
from sqlalchemy import desc

from .schemas import (
    dataset_schema,
    dataset_list_schema,
    tag_schema,
    tag_list_schema
)


class SingleDatasetView(SingleResourceByIdView):
    Model = Dataset
    Schema = dataset_schema

    def put(self, _id):
        '''Edit / Update the dataset with specified id.'''
        model_instance = self.Model.query.filter_by(id=_id).first_or_404()
        req_body = request.get_json()

        # Holds a list of tag ids to be updated. Tags will be added to the dataset manually
        updated_tags = req_body.pop('tags', None)

        # Test if updates are valid. If not, return error.
        try:
            self.Schema.load(req_body, instance=model_instance).data
        except ValidationError as err:
            return {'errors': err.messages}

        # TO_DO: Can delete tag if adding another tag. But can't solely delete a tag.
        # Front end issue maybe. A tag can only be deleted by adding another tag. Else the action won't be noticed.
        if updated_tags:
            model_instance.tags = [Tag.query.filter_by(id=tag_id).first() for tag_id in updated_tags]

        # Actually do the updates on the dataset and commit it.
        db.session.query(self.Model).filter_by(id=_id).update(dict(req_body))
        db.session.commit()

        return {
            'message': 'successfully updated',
            'updated': self.Schema.dump(model_instance)
        }


class ListDatasetView(ListResourceView):
    Model = Dataset
    ListSchema = dataset_list_schema
    SingleSchema = dataset_schema

    @jwt_optional
    def get(self):
        '''Returns datasets to be shown on homepage.'''

        # Only display unapproved datasets to admins
        is_admin = AdminOnly.has_permission(get_jwt_identity())
        if is_admin:
            query_list = self.Model.query
        else:
            query_list = self.Model.query.filter_by(is_approved=True)

        approved = request.args.get('approved')
        limit = request.args.get('limit', 50)
        offset = request.args.get('offset', 0)

        # Block non-admin users from seeing unapproved datasets through requests
        if approved == 'false':
            if is_admin:
                query_list = self.Model.query.filter_by(is_approved=False)
            else:
                return {
                    'error': 'Only admin can see datasets not yet approved',
                    'status': 401
                }, 401

        # Filter datasets by search inputs.
        search_param = request.args.get('search')
        if search_param is None:
            query_list = dataset_tag_filter(request, query_list)
            # datasets ordered by creation date - newest first (on top of page)
            query_list = query_list.order_by(desc(Dataset.date_created)).offset(offset).limit(limit)
        else:
            # datasets ordered by relevance
            # TODO: Allow search to search through certain indexes, not all
            query_list, total = Dataset.search(search_param)
            if not is_admin:
                query_list = query_list.filter_by(is_approved=True)
            query_list = dataset_tag_filter(request, query_list)
            query_list = query_list.offset(offset).limit(limit)

        # Put results in json format and return it
        model_list_json = self.ListSchema.dump(query_list)[0]
        return {
            'num_results': len(model_list_json),
            'results': model_list_json
        }, 200

    @jwt_required
    def post(self):
        '''Tries to create a dataset.'''
        req_body = request.get_json()
        # Holds a list of tag ids to be associated with the dataset.
        tags = req_body.pop('tags', [])

        # Add owner to dataset object
        # TODO: Store ID in JWT
        user = User.query.filter_by(username=get_jwt_identity()).first()
        req_body['owner'] = user.id

        # ValidationError is not raised when url / description is null.
        # Upgrade to marshmallow 3.0 when it becomes stable to fix.
        # https://github.com/marshmallow-code/marshmallow/milestone/10
        try:
            # Switch primary keys into actual model objects
            req_body['owner'] = User.query.filter_by(id=req_body['owner']).first()
            req_body['tags'] = [Tag.query.filter_by(id=tag_id).first() for tag_id in tags]
            # Load model
            new = Dataset(**req_body)
        except ValidationError as err:
            return {'errors': err.messages}
        else:

            db.session.add(new)
            db.session.commit()

        # send email to cove admin
        send_dataset_to_approve(Config.NOTIFY_ADMIN_EMAIL, req_body.get('name', 'Name Unavailable'))

        return {
            'message': 'successfully created',
            'new': self.SingleSchema.dump(new).data
        }


class ListTagView(ListResourceView):
    Model = Tag
    ListSchema = tag_list_schema
    SingleSchema = tag_schema

    def post(self):
        req_body = request.get_json()
        is_many = request.args.get('many') == 'true'

        if not is_many:
            req_body = [req_body]

        if len(req_body) is 0:
            return {
                'message': 'Nothing to create',
                'new': []
            }

        schema_to_use = self.ListSchema
        for tag in req_body:
            if tag.get('category', '') not in ['tasks', 'topics', 'data_types']:
                return {'errors': {"tags": ['Category must be in the list: ["tasks", "topics", "data_types"]']}}

        try:
            new = schema_to_use.load(req_body).data
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
            'new': schema_to_use.dump(new).data
        }


api.add_resource(SingleDatasetView, '/datasets/<_id>')
api.add_resource(ListDatasetView, '/datasets/')
api.add_resource(ListTagView, '/tags/')
