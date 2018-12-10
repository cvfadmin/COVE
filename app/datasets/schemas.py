from .models import Dataset, Tag
import flask_marshmallow.sqla as sqla


class TagSchema(sqla.ModelSchema):
    class Meta:
        model = Tag


class DatasetSchema(sqla.ModelSchema):

    class Meta:
        model = Dataset


dataset_schema = DatasetSchema()
dataset_list_schema = DatasetSchema(many=True)

tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
