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

        # 1.) Test if updates are valid without tags. If not, return error.
        try:
            updated_tags = req_body.pop('tags', None)
            self.Schema.load(req_body, instance=model_instance)
        except ValidationError as err:
            return {'errors': err.messages}

        # 2.) Create any new tags - validate new tags then create

        # New tags are defined by not having an id associated with the,
        new_tags_list = [tag for tag in updated_tags if tag.get('id', None) is None]
        old_tags_list = [tag for tag in updated_tags if tag.get('id') is not None]

        # There are tags that need to be created
        if len(new_tags_list) > 0:
            are_tags_validated, json_response = create_tags(new_tags_list)

            # Handle exception when creating new tags
            if not are_tags_validated:
                return json_response

            # Combine new tags with old tags
            all_tags = json_response['new'] + old_tags_list
        else:
            all_tags = old_tags_list

        # 3.) Validate dataset with tags and save
        try:
            # TO_DO: Can delete tag if adding another tag. But can't solely delete a tag.
            # Front end issue maybe. A tag can only be deleted by adding another tag. Else the action won't be noticed.
            model_instance.tags = [Tag.query.filter_by(id=tag["id"]).first() for tag in all_tags]
            updated = self.Schema.load(req_body, instance=model_instance)
        except ValidationError as err:
            return {'errors': err.messages}

        # Actually do the updates on the dataset and commit it.
        db.session.add(updated) # if it has the same primary key update is assumed
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
            total_results = query_list.count()
            # datasets ordered by creation date - newest first (on top of page)
            query_list = query_list.order_by(desc(Dataset.date_created)).offset(offset).limit(limit)
        else:
            # datasets ordered by relevance
            # TODO: Allow search to search through certain indexes, not all
            query_list, total = Dataset.search(search_param)
            if not is_admin:
                query_list = query_list.filter_by(is_approved=True)
            query_list = dataset_tag_filter(request, query_list)

            total_results = query_list.count()
            query_list = query_list.offset(offset).limit(limit)

        # Put results in json format and return it
        model_list_json = self.ListSchema.dump(query_list)

        return {
            'num_total_results': total_results,
            'num_page_results': len(model_list_json),
            'results': model_list_json
        }, 200

    @jwt_required
    def post(self):
        """ Tries to create a dataset. """

        # Jsonify request
        req_body = request.get_json()

        # Add owner to dataset request object
        user = User.query.filter_by(username=get_jwt_identity()).first()
        req_body['owner'] = user.id

        # 1.) Validate dataset without tags
        try:
            tags = req_body.pop('tags', None)
            self.SingleSchema.load(req_body)  # Call .rollback() to remove this from being loaded too
            db.session.rollback()
        except ValidationError as err:
            return {'errors': err.messages}

        # 2.) Create any new tags - validate new tags then create

        # New tags are defined by not having an id associated with the,
        new_tags_list = [tag for tag in tags if tag.get('id', None) is None]
        old_tags_list = [tag for tag in tags if tag.get('id') is not None]

        # There are tags that need to be created
        if len(new_tags_list) > 0:
            are_tags_validated, json_response = create_tags(new_tags_list)

            # Handle exception when creating new tags
            if not are_tags_validated:
                return json_response

            # Combine new tags with old tags
            all_tags = json_response['new'] + old_tags_list
        else:
            all_tags = old_tags_list

        # 3.) Validate dataset with tags and save
        try:

            req_body['tags'] = all_tags
            print(req_body)
            new = self.SingleSchema.load(req_body)
            print(new)

        except ValidationError as err:
            return {'errors': err.messages}

        db.session.add(new)
        db.session.commit()

        # send email to cove admin
        send_dataset_to_approve(Config.NOTIFY_ADMIN_EMAIL, req_body.get('name', 'Name Unavailable'))

        return {
            'message': 'successfully created',
            'new': self.SingleSchema.dump(new)
        }


def validate_tags(tag_list):
    """
    Validates a list of potential tag objects
    :return: (boolean, response json)
    """
    # Validate categories
    for tag in tag_list:
        if tag.get('category', '') not in ['tasks', 'topics', 'data_types']:
            return False, {'errors': {"tags": ['Category must be in the list: ["tasks", "topics", "data_types"]']}}

    # Enforce unique tags
    for tag in tag_list:
        if Tag.query.filter_by(name=tag.get('name')).count() > 0:
            return False, {'errors': {"tags": ["The tag: '" + tag.get('name') + "' already exists."]}}

    # Validate data with schema
    try:
        new = tag_list_schema.load(tag_list)
    except ValidationError as err:
        return False, {'errors': err.messages}

    return True, new


def create_tags(tag_list):
    """
    Tries to create tags
    :param tag_list: List of potential tag objects
    :param is_many: Boolean - Is there only one tag in list or > 1
    :return: Response JSON
    """

    is_validated, data = validate_tags(tag_list)

    if not is_validated:
        return is_validated, data

    for new_model in data:
        db.session.add(new_model)
        db.session.commit()

    return is_validated, {
        'message': 'successfully created',
        'new': tag_list_schema.dump(data)
    }


class ListTagView(ListResourceView):
    Model = Tag
    ListSchema = tag_list_schema
    SingleSchema = tag_schema

    def post(self):
        is_many = request.args.get('many') == 'true'  # TODO: This may be unecassary
        req_body = request.get_json() if is_many else [request.get_json()]

        if len(req_body) is 0:
            return {'message': 'Nothing to create', 'new': []}

        # Factored out this logic so dataset view can also create tags
        _, json_response = create_tags(req_body)
        return json_response


api.add_resource(SingleDatasetView, '/datasets/<_id>')
api.add_resource(ListDatasetView, '/datasets/')
api.add_resource(ListTagView, '/tags/')
