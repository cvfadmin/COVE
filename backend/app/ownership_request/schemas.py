from .models import OwnershipRequest
from marshmallow import fields
import flask_marshmallow.sqla as sqla
from app import ma


class OwnershipRequestSchema(sqla.ModelSchema):
    class Meta:
        model = OwnershipRequest

    dataset_name = fields.Function(lambda obj: obj.dataset.name)
    author_name = fields.Function(lambda obj: f'{obj.author.first_name} {obj.author.last_name}, ({obj.author.username})')
    author_email = fields.Function(lambda obj: obj.author.email)

ownership_request_schema = OwnershipRequestSchema()
ownership_requests_schema = OwnershipRequestSchema(many=True)
