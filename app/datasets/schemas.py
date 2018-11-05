from .models import Dataset, AddDatasetRequest, DeleteDatasetRequest
import flask_marshmallow.sqla as sqla


class DatasetSchema(sqla.ModelSchema):
    class Meta:
        model = Dataset


class AddDatasetRequestSchema(sqla.ModelSchema):
    class Meta:
        model = AddDatasetRequest


class DeleteDatasetRequestSchema(sqla.ModelSchema):
    class Meta:
        model = DeleteDatasetRequest


dataset_schema = DatasetSchema()
dataset_list_schema = DatasetSchema(many=True)

add_dataset_request_schema = AddDatasetRequestSchema()
add_dataset_request_list_schema = DeleteDatasetRequestSchema(many=True)

delete_dataset_request_schema = DeleteDatasetRequestSchema()
delete_dataset_request_list_schema = DeleteDatasetRequestSchema(many=True)
