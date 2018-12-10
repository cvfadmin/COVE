from app import api, db
from flask import request
from marshmallow import ValidationError
from app.lib.routes import SingleResourceByIdView, ListResourceView
from app.auth.models import User
from .models import Dataset, Tag
from app.auth.permissions import AdminOnly
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from .filter import dataset_tag_filter

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
        model_instance = self.Model.query.filter_by(id=_id).first_or_404()
        req_body = request.get_json()
        updated_tags = req_body.pop('tags', None)

        try:
            self.Schema.load(req_body, instance=model_instance)
        except ValidationError as err:
            return {'errors': err.messages}

        # TODO: Clean this up
        if updated_tags:
            tag_instances = []
            for tag_id in req_body['tags']:
                tag_instances.append(Tag.query.filter_by(id=tag_id).first())
            model_instance.tags = tag_instances

        db.session.query(self.Model).filter_by(id=_id).update(req_body)
        db.session.commit()

        return {
            'message': 'successfully created',
            'updated': self.Schema.dump(model_instance)
        }


class ListDatasetView(ListResourceView):
    Model = Dataset
    ListSchema = dataset_list_schema
    SingleSchema = dataset_schema

    @jwt_optional
    def get(self):
        is_admin = AdminOnly.has_permission(get_jwt_identity())
        if is_admin:
            query_list = self.Model.query
        else:
            query_list = self.Model.query.filter_by(is_approved=True)

        approved = request.args.get('approved')
        if approved == 'false':
            if is_admin:
                query_list = self.Model.query.filter_by(is_approved=False)
            else:
                return {
                    'error': 'Only admin can see datasets not yet approved',
                    'status': 401
                }, 401

        search_param = request.args.get('search')
        if search_param is not None:
            query_list = Dataset.query.whooshee_search(search_param, order_by_relevance=-1).all()

        query_list = dataset_tag_filter(request, query_list)
        model_list_json = self.ListSchema.dump(query_list)
        return {
            'num_results': len(model_list_json),
            'results': model_list_json
        }, 200

    @jwt_required
    def post(self):
        req_body = request.get_json()

        # Add owner to dataset object
        # TODO: Store ID in JWT
        user = User.query.filter_by(username=get_jwt_identity()).first()
        req_body['owner'] = user.id

        try:
            new = self.SingleSchema.load(req_body)
        except ValidationError as err:
            return {'errors': err.messages}
        else:
            db.session.add(new)
            db.session.commit()

        return {
            'message': 'successfully created',
            'new': self.SingleSchema.dump(new)
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

        schema_to_use = self.ListSchema

        for tag in req_body:
            if tag.get('category', '') not in ['tasks', 'topics', 'data_types']:
                return {'errors': {"tags": ['Category must be in the list: ["tasks", "topics", "data_types"]']}}

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


api.add_resource(SingleDatasetView, '/datasets/<_id>')
api.add_resource(ListDatasetView, '/datasets/')
api.add_resource(ListTagView, '/tags/')