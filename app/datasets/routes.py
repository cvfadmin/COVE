from app import api, db
from flask import request
from marshmallow import ValidationError
from ..lib.routes import SingleResourceByIdView, ListResourceView
from .models import Dataset, AddDatasetRequest, DeleteDatasetRequest, Tag, EditDatasetRequest
from app.auth.permissions import AdminOnly
from flask_jwt_extended import jwt_optional, get_jwt_identity
from app.admin.models import CreateDatasetKey
from .filter import dataset_tag_filter

from .schemas import (
    dataset_schema,
    add_dataset_request_schema,
    delete_dataset_request_schema,
    add_dataset_request_list_schema,
    delete_dataset_request_list_schema,
    dataset_list_schema,
    edit_dataset_request_schema,
    edit_dataset_request_list_schema,
    tag_schema,
    tag_list_schema
)


class SingleDatasetView(SingleResourceByIdView):
    Model = Dataset
    Schema = dataset_schema


class SingleAddDatasetRequestView(SingleResourceByIdView):
    Model = AddDatasetRequest
    Schema = add_dataset_request_schema


class SingleDeleteDatasetRequestView(SingleResourceByIdView):
    Model = DeleteDatasetRequest
    Schema = delete_dataset_request_schema


class SingleEditDatasetRequestView(SingleResourceByIdView):
    Model = EditDatasetRequest
    Schema = edit_dataset_request_schema


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

    def post(self):
        req_body = request.get_json()
        print(req_body)
        key = req_body.pop('key', None)
        create_ds_key = CreateDatasetKey.query.filter_by(key=key).first()

        if create_ds_key is not None:
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
        else:
            return {'error': 'Key invalid'}, 401


class ListAddDatasetRequestView(ListResourceView):
    Model = AddDatasetRequest
    ListSchema = add_dataset_request_list_schema
    SingleSchema = add_dataset_request_schema


class ListDeleteDatasetRequestView(ListResourceView):
    Model = DeleteDatasetRequest
    ListSchema = delete_dataset_request_list_schema
    SingleSchema = delete_dataset_request_schema


class ListEditDatasetRequestView(ListResourceView):
    Model = EditDatasetRequest
    ListSchema = edit_dataset_request_list_schema
    SingleSchema = edit_dataset_request_schema


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
            print(tag)
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
api.add_resource(SingleAddDatasetRequestView, '/requests/add-dataset/<_id>')
api.add_resource(SingleEditDatasetRequestView, '/requests/edit-dataset/<_id>')
api.add_resource(SingleDeleteDatasetRequestView, '/requests/delete-dataset/<_id>')

api.add_resource(ListDatasetView, '/datasets/')
api.add_resource(ListAddDatasetRequestView, '/requests/add-dataset')
api.add_resource(ListEditDatasetRequestView, '/requests/edit-dataset')
api.add_resource(ListDeleteDatasetRequestView, '/requests/delete-dataset')
api.add_resource(ListTagView, '/tags/')