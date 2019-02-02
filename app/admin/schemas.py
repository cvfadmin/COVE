from .models import EditRequestMessage, EditRequest
from marshmallow import fields
import flask_marshmallow.sqla as sqla
from app import ma


class EditRequestMessageSchema(sqla.ModelSchema):
    class Meta:
        model = EditRequestMessage

    date_created = fields.DateTime(dump_only=True)

class EditRequestSchema(sqla.ModelSchema):
    class Meta:
        model = EditRequest

    messages = ma.Nested(EditRequestMessageSchema, many=True)


edit_request_message_schema = EditRequestMessageSchema()
edit_request_messages_schema = EditRequestMessageSchema(many=True)

edit_request_schema = EditRequestSchema()
edit_requests_schema = EditRequestSchema(many=True)
