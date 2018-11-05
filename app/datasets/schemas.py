from .models import Dataset, AddDatasetRequest
import flask_marshmallow.sqla as sqla


class DatasetSchema(sqla.ModelSchema):
    class Meta:
        model = Dataset


class AddDatasetRequestSchema(sqla.ModelSchema):
    class Meta:
        model = AddDatasetRequest


dataset_schema = DatasetSchema()
add_dataset_request_schema = AddDatasetRequestSchema()
