from .models import Dataset, Tag
from app.admin.schemas import EditRequestSchema
import flask_marshmallow.sqla as sqla
from app import ma


class TagSchema(sqla.ModelSchema):
    class Meta:
        model = Tag


class DatasetSchema(sqla.ModelSchema):
    class Meta:
        model = Dataset

    edit_requests = ma.Nested(EditRequestSchema, many=True)


dataset_schema = DatasetSchema()
dataset_list_schema = DatasetSchema(many=True)

tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
