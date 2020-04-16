from app import ma
from app.auth.models import User

from marshmallow import fields
import flask_marshmallow.sqla as sqla

from .models import EditRequestMessage, EditRequest


class EditRequestMessageSchema(sqla.ModelSchema):
    class Meta:
        model = EditRequestMessage

    author_name = fields.Function(lambda obj: obj.author.username)


class EditRequestSchema(sqla.ModelSchema):
    class Meta:
        model = EditRequest

    messages = ma.Nested(EditRequestMessageSchema, many=True)
    dataset_name = fields.Function(lambda obj: obj.dataset.name)


edit_request_message_schema = EditRequestMessageSchema()
edit_request_messages_schema = EditRequestMessageSchema(many=True)

edit_request_schema = EditRequestSchema()
edit_requests_schema = EditRequestSchema(many=True)


class AdminUserSchema(sqla.ModelSchema):
    class Meta:
        model = User

users_schema = AdminUserSchema(many=True)