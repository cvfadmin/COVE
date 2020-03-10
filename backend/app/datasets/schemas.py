from .models import Dataset, Tag
from app.admin.schemas import EditRequestSchema
from app import ma
from marshmallow import fields


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag


class DatasetSchema(ma.ModelSchema):
    class Meta:
        model = Dataset

    edit_requests = ma.Nested(EditRequestSchema, many=True)
    tags = ma.Nested(TagSchema, many=True)
    is_owned_by_admin = fields.Function(lambda obj: obj.owner.is_admin)


dataset_schema = DatasetSchema()
dataset_list_schema = DatasetSchema(many=True)

tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
