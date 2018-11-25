from .models import Dataset, AddDatasetRequest, DeleteDatasetRequest, Tag, EditDatasetRequest
import flask_marshmallow.sqla as sqla


class TagSchema(sqla.ModelSchema):
    class Meta:
        model = Tag


class DatasetSchema(sqla.ModelSchema):

    class Meta:
        model = Dataset


class AddDatasetRequestSchema(sqla.ModelSchema):
    class Meta:
        model = AddDatasetRequest


class DeleteDatasetRequestSchema(sqla.ModelSchema):
    class Meta:
        model = DeleteDatasetRequest


class EditDatasetRequestSchema(sqla.ModelSchema):
    class Meta:
        model = EditDatasetRequest



dataset_schema = DatasetSchema()
dataset_list_schema = DatasetSchema(many=True)

add_dataset_request_schema = AddDatasetRequestSchema()
add_dataset_request_list_schema = AddDatasetRequestSchema(many=True)

delete_dataset_request_schema = DeleteDatasetRequestSchema()
delete_dataset_request_list_schema = DeleteDatasetRequestSchema(many=True)

edit_dataset_request_schema = EditDatasetRequestSchema()
edit_dataset_request_list_schema = EditDatasetRequestSchema(many=True)

tag_schema = TagSchema()
tag_list_schema = TagSchema(many=True)
