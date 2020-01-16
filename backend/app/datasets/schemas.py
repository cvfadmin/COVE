from .models import Dataset, Tag
from app.admin.schemas import EditRequestSchema
from app import ma


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag


class DatasetSchema(ma.ModelSchema):
    class Meta:
        model = Dataset

    edit_requests = ma.Nested(EditRequestSchema, many=True)
    tags = ma.Nested(TagSchema, many=True)


dataset_schema = DatasetSchema()
dataset_list_schema = DatasetSchema(many=True)

tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
