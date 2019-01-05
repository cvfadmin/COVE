from .models import EditRequestMessage, EditRequest
import flask_marshmallow.sqla as sqla
from app import ma


class EditRequestMessageSchema(sqla.ModelSchema):
    class Meta:
        model = EditRequestMessage

class EditRequestSchema(sqla.ModelSchema):
    class Meta:
        model = EditRequest

    messages = ma.Nested(EditRequestMessageSchema, many=True)


edit_request_message_schema = EditRequestMessageSchema()
edit_request_messages_schema = EditRequestMessageSchema(many=True)

edit_request_schema = EditRequestSchema()
edit_requests_schema = EditRequestSchema(many=True)
